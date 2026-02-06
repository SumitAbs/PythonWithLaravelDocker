from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import hash_password # Import our hashing utility

from datetime import timedelta
from fastapi.security import OAuth2PasswordRequestForm
from app.core.security import verify_password, create_access_token

# Corrected Professional Imports
from app.core.database import SessionLocal, engine, Base 
from app.models import user as models
from app.schemas import user as schemas

# Initialize database tables using the modular path
models.Base.metadata.create_all(bind=engine)


app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Professional Modular API is online!"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Standard practice: check for existing email
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # 2. Hash the password
    hashed_pwd = hash_password(user.password)

    new_user = models.User(
        name=user.name,
        email=user.email,
        hashed_password=hashed_pwd
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    return db.query(models.User).all()

@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db_user.name = updated_user.name
    db_user.email = updated_user.email
    
    db.commit()
    db.refresh(db_user)
    return db_user

@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(db_user)
    db.commit()
    return {"message": f"User with ID {user_id} successfully deleted"}

# GET a single user profile by ID (Equivalent to Laravel's show method)
@app.get("/users/{user_id}", response_model=schemas.UserResponse)
def get_user_profile(user_id: int, db: Session = Depends(get_db)):
    """
    Fetch a single user profile by their primary key.
    """
    # 1. Query the database for the specific user
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    
    # 2. If the user does not exist, throw a 404 error
    if not db_user:
        raise HTTPException(status_code=404, detail="User profile not found")
    
    return db_user

@app.post("/users/{user_id}/tasks/", response_model=schemas.TaskResponse)
def create_task_for_user(
    user_id: int, 
    task: schemas.TaskCreate, 
    db: Session = Depends(get_db)
):
    """
    Creates a task owned by a specific user.
    Equivalent to $user->tasks()->create([...]) in Laravel.
    """
    new_task = models.Task(**task.model_dump(), owner_id=user_id)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task


@app.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(get_db)
):
    # 1. Look for the user in the database by email [cite: 2026-02-02]
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    
    # 2. Verify if user exists and if the provided password matches the hash [cite: 2026-02-02]
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # 3. Generate the JWT token [cite: 2026-02-02]
    access_token = create_access_token(data={"sub": user.email})
    
    return {"access_token": access_token, "token_type": "bearer"}
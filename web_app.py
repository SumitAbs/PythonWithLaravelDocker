from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, User, create_tables
import schemas

# Initialize database tables
create_tables()

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
    return {"message": "Database API is active!"}

@app.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    Creates a new user in the database.
    Equivalent to: User::create(['name' => $name, 'email' => $email]) in Laravel.
    """

    # Check if user already exists (Standard API practice)
    db_user = db.query(User).filter(User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Create a new User instance
    new_user = User(name=user.name, email=user.email)
    
    # Add to session and commit to database
    db.add(new_user)
    db.commit()
    
    # Refresh to get the generated ID
    db.refresh(new_user)
    
    return new_user

@app.get("/users/", response_model=list[schemas.UserResponse])
def get_all_users(db: Session = Depends(get_db)):
    """
    Fetches all user records from the database.
    Equivalent to: User::all() in Laravel.
    """
    # Query the database for all records in the User table
    users = db.query(User).all()
   
    return users

# UPDATE a user (Equivalent to Laravel's update method)
@app.put("/users/{user_id}", response_model=schemas.UserResponse)
def update_user(user_id: int, updated_user: schemas.UserUpdate, db: Session = Depends(get_db)):
    # 1. Fetch the user from the database
    db_user = db.query(User).filter(User.id == user_id).first()
    
    # 2. Raise 404 error if user doesn't exist
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 3. Update the fields
    db_user.name = updated_user.name
    db_user.email = updated_user.email
    
    # 4. Commit and Refresh the record
    db.commit()
    db.refresh(db_user)
    return db_user

# DELETE a user (Equivalent to Laravel's destroy method)
@app.delete("/users/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    # 1. Fetch the user
    db_user = db.query(User).filter(User.id == user_id).first()
    
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 2. Remove the user and commit
    db.delete(db_user)
    db.commit()
    
    return {"message": f"User with ID {user_id} successfully deleted"}
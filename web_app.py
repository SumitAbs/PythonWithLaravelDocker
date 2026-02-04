from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database import SessionLocal, User, create_tables

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

@app.post("/users/")
def create_user(name: str, email: str, db: Session = Depends(get_db)):
    """
    Creates a new user in the database.
    Equivalent to: User::create(['name' => $name, 'email' => $email]) in Laravel.
    """
    # Create a new User instance
    new_user = User(name=name, email=email)
    
    # Add to session and commit to database
    db.add(new_user)
    db.commit()
    
    # Refresh to get the generated ID
    db.refresh(new_user)
    
    return {"status": "User created", "user": new_user}

@app.get("/users/")
def get_all_users(db: Session = Depends(get_db)):
    """
    Fetches all user records from the database.
    Equivalent to: User::all() in Laravel.
    """
    # Query the database for all records in the User table
    users = db.query(User).all()
   
    return {"total_users": len(users), "users": users}

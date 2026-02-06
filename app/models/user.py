from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

    # Professional Comment: Define the relationship to Tasks
    # Equivalent to $this->hasMany(Task::class) in Laravel
    tasks = relationship("Task", back_populates="owner")

class Task(Base):
    __tablename__ = "tasks"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    
    # Foreign Key linking to the User
    owner_id = Column(Integer, ForeignKey("users.id"))

    # Define the relationship back to the User
    # Equivalent to $this->belongsTo(User::class) in Laravel
    owner = relationship("User", back_populates="tasks")
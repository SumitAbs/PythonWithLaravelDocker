from pydantic import BaseModel, EmailStr

# Base schema for shared User properties
class UserBase(BaseModel):
    name: str
    email: EmailStr
# Data required to create a new user (includes password)
class UserCreate(UserBase):
    password: str # Required for registration but not stored in this class

# Data structure for updating an existing user
class UserUpdate(UserBase):
    pass # Inherits name and email from UserBase


# Task Schemas
class TaskCreate(BaseModel):
    title: str
    description: str | None = None

class TaskResponse(BaseModel):
    id: int
    title: str
    description: str | None
    owner_id: int

    class Config:
        from_attributes = True

# Response schema that nests tasks [cite: 2026-02-02]
class UserResponse(UserBase):
    id: int
    tasks: list[TaskResponse] = [] # Nested relationship [cite: 2026-02-02]

    class Config:
        from_attributes = True
 
from pydantic import BaseModel, EmailStr

# Professional Comment: Data required to create a new user
class UserCreate(BaseModel):
    name: str
    email: EmailStr

# Professional Comment: Data structure for updating an existing user
class UserUpdate(BaseModel):
    name: str
    email: EmailStr


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

# Update UserResponse to optionally show their tasks
class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    tasks: list[TaskResponse] = [] # This nests the tasks inside the user JSON!

    class Config:
        from_attributes = True
 
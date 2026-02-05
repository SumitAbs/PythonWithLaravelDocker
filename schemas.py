from pydantic import BaseModel, EmailStr

# Professional Comment: This schema defines what the API expects from the user
class UserCreate(BaseModel):
    name: str
    email: EmailStr  # This automatically validates email format!

# Professional Comment: This schema defines what the API sends back to the user
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        # This allows Pydantic to read data from SQLAlchemy models
        from_attributes = True
from pydantic import BaseModel, EmailStr

# Professional Comment: Data required to create a new user [cite: 2026-02-02]
class UserCreate(BaseModel):
    name: str
    email: EmailStr

# Professional Comment: Data structure for updating an existing user [cite: 2026-02-02]
class UserUpdate(BaseModel):
    name: str
    email: EmailStr

# Professional Comment: Data structure sent back in API responses [cite: 2026-02-02]
class UserResponse(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        from_attributes = True
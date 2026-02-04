from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the database connection URL (SQLite for local development)
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

# Create the SQLAlchemy engine
# Professional Comment: 'check_same_thread' is required only for SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a SessionLocal class for database transactions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for our database models to inherit from
Base = declarative_base()

# Define the User Model (Equivalent to a Laravel Migration + Model)
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    email = Column(String, unique=True, index=True)

# Function to create the tables in the database
def create_tables():
    Base.metadata.create_all(bind=engine)
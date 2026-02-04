from fastapi import FastAPI
from utils.api_client import get_post_data

# Initialize the FastAPI application
app = FastAPI()

@app.get("/")
def read_root():
    """
    Default landing route.
    """
    return {"message": "Welcome to your first Python Web API!"}

@app.get("/post/{post_id}")
def read_post(post_id: int):
    """
    Route that fetches data using our existing utility module.
    """
    data = get_post_data(post_id)
    return {"source": "External API", "data": data}
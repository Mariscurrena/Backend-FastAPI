from pydantic import BaseModel

class User(BaseModel):
    # Neccesary define the None=None for optional values
    id: str | None = None # Assign direct for MongoDB, that's cause it's optional
    username: str 
    email: str
from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt

app = FastAPI()
oauth2 =  OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str 
    email: str
    disabled: bool

class UserDB (User): # Heredates from user
    password: str

users_db = {
    "steve": {
        "username": "steve",
        "full_name": "Angel Mariscurrena", 
        "email": "mariscurrena@gmail.com",
        "disabled": False,
        "password": "admin1234"
    },
    "steve2": {
        "username": "steve2",
        "full_name": "Angel Mariscurrena 2", 
        "email": "mariscurrena2@gmail.com",
        "disabled": True,
        "password": "1234admin"
    }
}

def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    
    user = search_user_db(form.username)

    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    return {"access_token": user.username, "token_type": "bearer"}

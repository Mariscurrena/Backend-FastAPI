from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta

#Encrypt algorithm
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1 ## An access_token has an expiration period associated
SECRET = "ec9be770107c1414fc85f41c3c108d15d0b0b8f722c9ec3415ae4f04c5b7d8bc" # Proper way - openssl rand -hex 32 -> Useful for generate secrets

router = APIRouter( prefix="/jwtauth",
                    tags=["jwtauth"])
oauth2 =  OAuth2PasswordBearer(tokenUrl="login")

#Encryption context
crypt = CryptContext(schemes=["bcrypt"]) # Schemas define the encryption algorithm that will be used

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
        "password": "$2a$12$PhAihgSB9chRTK4SDq03BuxxraIzUlFpJaggPO1hlzAbE41TFfxNK" ## https://bcrypt-generator.com/ - admin1234
    },
    "steve2": {
        "username": "steve2",
        "full_name": "Angel Mariscurrena 2", 
        "email": "mariscurrena2@gmail.com",
        "disabled": True,
        "password": "$2a$12$TdAfxwCij5V3QuWRL4JbCeSJ0A7nCutNutAW.g8pFHN83rycKFRS2" ## https://bcrypt-generator.com/ - 1234admin
    }
}

# Returns an DB instance with pass
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

#Returns instance without pass
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# TOKEN VALIDATION PROCESS: Validates auth with token and returns the decoded user data.
async def auth_user(token: str  = Depends(oauth2)): # Depends of the token given at "/login" endpoint
    ## Based on the token, it should be decoded in order to find the data
    exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, 
            detail="Invalid Authentication - JWT Token", 
            headers={"WWW-Authenticate": "Bearer"}) 
    try:
        username = jwt.decode(token, SECRET, algorithms=ALGORITHM).get("sub")
        if username is None: # If the username is empty, raise an exception
            raise exception 
    except JWTError:
        raise exception
    
    return search_user(username) ## If no exception happened, call "search_user" and return an User instance (Doesn't have password there)

# Recieves the decoded data user and validates if its disabled, if not return user object
async def current_user(user: User = Depends(auth_user)): 
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has been disabled."
        )
    return user


@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db: 
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    
    user = search_user_db(form.username)

    ## Due to "Crypt" is the encryption context, verify method already knows what encryption method use for comparing with the input user password
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")

    access_token_expiration = timedelta(minutes=ACCESS_TOKEN_DURATION) # Creates a Delta that is a minute advanced than the current time
    expire = datetime.utcnow() + access_token_expiration #Instance for expire in one exact minute based on the access_token_expiration
    
    access_token = {
        "sub":user.username,
        "exp":expire,
    }

    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"} # jwt library allows to perform the encode and decode

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel
# OAuth2PasswordBearer - Manages user and password in order to perform auth
# OAuth2PasswordRequestForm - How the auth criteria will be send to the backend
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

router = APIRouter(tags=["Basic Auth"])

# Auth Instance
oauth2 =  OAuth2PasswordBearer(tokenUrl="login")

# Data that is send through Network
class User(BaseModel):
    username: str
    full_name: str 
    email: str
    disabled: bool

# Data that cannot be sent in an unprotected way
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

# Validates if user exists
def search_user_db(username: str):
    if username in users_db: # Just a demostrative approach, into a realistic one, it would be better use and algorithm such as Binary search
        return UserDB(**users_db[username]) # Creates a UserDB instance according to the existing user
        # The ** represents the arbitrary parameter number that should be used for create the object

# Function for return a non DBUser in order to do not compromise the password
def search_user(username: str):
    if username in users_db:
        return User(**users_db[username]) 

# Dependance criteria
async def current_user(token: str = Depends(oauth2)): # Needs authorization token from user
    user = search_user(token) ## This is useful in this particular and demonstrative case just because the token is the username, in a productive or realistic escenario should be different the token validation
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, # status -> Useful for work with code status without memorizing
            detail="Invalid Authentication - Bearer Token", 
            headers={"WWW-Authenticate": "Bearer"}) # headers -> Standard
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User has been disabled."
        )
    return user

@router.post("/loginbasic")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Used as a criteria of authorization and access to resources according to the scope
    user_db = users_db.get(form.username)
    if not user_db: # If user isn't in DB, user doesn't exist
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect username")
    
    # If user does exist
    user = search_user_db(form.username)

    # Password validation
    if not form.password == user.password: # Using db user
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect password")
    
    # If password is correct, response with a bearer token
    return {"access_token": user.username, "token_type": "bearer"}


# Operation for request username once authenticated
@router.get("/usersbasic/me")
async def me(user: User = Depends(current_user)): # Dependance criteria 
    return user # Will not have an user to return if current_user criteria does't respond with an actual user
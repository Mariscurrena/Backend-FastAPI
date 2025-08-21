from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["UsersDB"],
                   responses={status.HTTP_400_BAD_REQUEST: {"message": "An error has occured"}})

users_list = []

@router.get("/all", response_model=list[User]) ## Specify that I want to return a list of users as an expected response
async def users():
    return users_schema(db_client.local.users.find())

@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))
    
@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED) 
async def user(user: User):
    if type(search_user("email", user.email)) == User:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User already exists")
    
    user_dict = dict(user) #As use pydantic, it's transformate to the needed MOdel (JSON)
    del user_dict["id"] # Errase ID due to it's automatic assign

    id = db_client.local.users.insert_one(user_dict).inserted_id #Mongo instance - Schema, add inserted id

    new_user = user_schema(db_client.local.users.find_one({"_id":id})) # Looks for new user (id) in the DB, and returns a JSONS
    #ID in mongo is "_id

    return User(**new_user) ## Returns an user object

@router.put("/", response_model=User, status_code=status.HTTP_202_ACCEPTED)
async def user(user: User):
    found = False ## Initial logic condition
    for index, saved_user in enumerate(users_list): ## Looking for user
        if saved_user.id == user.id: ## If condition meets
            users_list[index] = user ## User is updated
            found = True ## Logic condition changed

    if not found: ## If logic condition not changed, user was not modified
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has not been updated")
    else:
        return user
    
@router.delete("/{id}", status_code=status.HTTP_202_ACCEPTED)
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list): ## Looking for user
        if saved_user.id == id: ## If condition meets
            del users_list[index] ## User is deleted
            found = True ## Logic condition changed

    if not found:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has not been deleted")
    else:
        return {"warning": "User was deleted"}
    

# Search function that validates if the user already exists
def search_user(field: str, key):  ## Performing a generic function to be able to reuse it
    try: 
        user = user_schema(db_client.local.users.find_one({field: key})) # Perform transformation based on search criteria
        return User(**user) # Return user as a User instance of base model
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
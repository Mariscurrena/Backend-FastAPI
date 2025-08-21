from fastapi import APIRouter, HTTPException, status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema, users_schema
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                   tags=["UsersDB"],
                   responses={status.HTTP_400_BAD_REQUEST: {"message": "An error has occured"}})

users_list = []

#-READ ALL-###########################################################################################################################
@router.get("/all", response_model=list[User]) ## Specify that I want to return a list of users as an expected response
async def users():
    return users_schema(db_client.local.users.find())

#-READ PATH-###########################################################################################################################
@router.get("/{id}")
async def user(id: str):
    return search_user("_id", ObjectId(id))

#-READ QUERY-###########################################################################################################################
@router.get("/")
async def user(id: str):
    return search_user("_id", ObjectId(id))

#-CREATE USER-###########################################################################################################################
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

#-UPDATE ALL USER-###########################################################################################################################
@router.put("/", response_model=User, status_code=status.HTTP_202_ACCEPTED)
async def user(user: User):
    user_dict = dict(user) #Transform user input into a dictionary for being handle by mongo
    del user_dict["id"] #Delete ID because it can not change
    try:
        db_client.local.users.find_one_and_replace({"_id": ObjectId(user.id)}, user_dict) # Save user_dict, new parameter from user
    except:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has not been updated")   
    
    return search_user("_id", ObjectId(user.id))  

#-DELETE USER-########################################################################################################################### 
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def user(id: str):
    found = db_client.local.users.find_one_and_delete({"_id": ObjectId(id)})

    if not found: ## Mongo API returns deleted value when deleted successfully, so if not, found is empty and raise an error
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="User has not been deleted")
    

# Search function that validates if the user already exists based on the given field type
def search_user(field: str, key):  ## Performing a generic function to be able to reuse it
    try: 
        user = user_schema(db_client.local.users.find_one({field: key})) # Perform transformation based on search criteria
        return User(**user) # Return user as a User instance of base model
    except:
        return HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
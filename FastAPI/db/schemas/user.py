### Function for return in a proper way the object, mainly for mongo syntax
#### Return should be a string type, because it's the defined args for User model
def user_schema(user) -> dict:
    return {
        "id": str(user["_id"]), #ID in Mongo are objects
        "username": user["username"],
        "email": user["email"]
    }

def users_schema(users) -> list:
    return [user_schema(user) for user in users] # For each user received in array, a transformation will be performed
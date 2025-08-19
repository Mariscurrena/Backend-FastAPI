from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

### With FastAPI and pydantic is possible create an Object and use it instead direct JSON
class User(BaseModel): ###Base Model helps to create an entity without needing define constructors like in a conventional class
    id: int
    name: str 
    surname: str
    url: str
    age: int ### Using Type Hints

### Imaginary users instead of connect the DB
users_list = [User(id=1, name="Angel", surname="Mariscurrena", url="https://mariscurrena.github.io/Portfolio-AM/", age=24),
              User(id=2, name="Andrea", surname="Trujillo", url="https://mariscurrena.github.io/Portfolio-AM/", age=24),
              User(id=3, name="Emilio", surname="Mariscurrena", url="https://mariscurrena.github.io/Portfolio-AM/", age=12)] ### Creates instances of User class

###Example of how to work directly with JSON, not the best option in a OOP language
@app.get("/usersjson")
async def usersjson():
    return [
        {
        "name":"Angel",
        "surname":"Mariscurrena",
        "url":"https://mariscurrena.github.io/Portfolio-AM/",
        "age": 24
        },
        {
        "name":"Andrea",
        "surname":"Trujillo",
        "url":"https://mariscurrena.github.io/Portfolio-AM/",
        "age": 24
        },
        {
        "name":"Emilio",
        "surname":"Mariscurrena",
        "url":"https://mariscurrena.github.io/Portfolio-AM/",
        "age": 12
        }
    ]

@app.get("/users")
async def users():
    #return User(name="Angel", surname="Mariscurrena", url="https://mariscurrena.github.io/Portfolio-AM/", age=24) #Instance for an specific user using User's class
    return users_list

### Call from path
### This block allows calling search function from path or form query equaly
@app.get("/user/{id}")
async def user(id: int):
    return search_user(id)
    
### Call from query
### Initialize a parameter from URL with "?" operator
@app.get("/user/")
async def user(id: int):
    return search_user(id)
    
### Reusable function for API endpoints "user" and "userquery"
def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list) #Filter = Superior order function
    try: ## Handles errors for unexisting users
        return list(users)[0] ## Return a list with the filter function using lambda function results, just the first element of the list (object)
    except:
        return {"error": "User has not been found"}
    
### (Example) Combining Path and Query parameters
# @app.get("/userpq/{id}")
# async def userpq(id: int, name: str):
#     users = filter(lambda user: user.id == id and user.name == name, users_list)
#     try:
#         return list(users)[0]
#     except:
#         return {"error": "User has not been found"}

###### POST Request
@app.post("/user/",status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User: ### Input validation for existing users
        raise HTTPException(status_code=204, detail="User already exists") ### No content
    else:
        users_list.append(user)
        return user
#### POST Data example
# {
#   "id":4, 
#   "name":"Elizabeth", 
#   "surname":"Cercado", 
#   "url":"https://mariscurrena.github.io/Portfolio-AM/", 
#   "age":47
# }


###### PUT Request
@app.put("/user/",)
async def user(user: User):
    ### Basic programming
    found = False ## Initial logic condition
    for index, saved_user in enumerate(users_list): ## Looking for user
        if saved_user.id == user.id: ## If condition meets
            users_list[index] = user ## User is updated
            found = True ## Logic condition changed

    if not found: ## If logic condition not changed, user was not modified
        raise HTTPException(status_code=409, detail="User has not been updated")
    else:
        return user
    

###### DELETE Request
@app.delete("/user/{id}", status_code=202)
async def user(id: int):
    found = False
    for index, saved_user in enumerate(users_list): ## Looking for user
        if saved_user.id == id: ## If condition meets
            del users_list[index] ## User is deleted
            found = True ## Logic condition changed

    if not found:
        raise HTTPException(status_code=409, detail="User has not been deleted")
    else:
        return {"warning": "User was deleted"}
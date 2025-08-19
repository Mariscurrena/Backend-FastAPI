from fastapi import FastAPI
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

@app.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list) #Filter = Superior order function
    try: ## Handles errors for unexisting users
        return list(users)[0] ## Return a list with the filter function using lambda function results, just the first element of the list (object)
    except:
        return {"error": "User has not been found"}
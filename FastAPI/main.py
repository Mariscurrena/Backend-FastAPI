from fastapi import FastAPI
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)
app.include_router(users_db.router)
app.include_router(jwt_auth_users.router) #Auth JWT router
app.include_router(basic_auth_users.router) #Auth Basic router

# Static Resources
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def root():
    return "Hi, FastAPI!"

@app.get("/response")
async def response():
    return { "url":"https://www.google.com"  }
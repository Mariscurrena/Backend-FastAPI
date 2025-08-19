from fastapi import FastAPI
from routers import products, users

app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(users.router)

@app.get("/")
async def root():
    return "Hi, FastAPI!"

@app.get("/response")
async def response():
    return { "url":"https://www.google.com"  }
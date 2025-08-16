from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return "Hi, FastAPI!"

@app.get("/response")
async def response():
    return { "url":"https://www.google.com"  }
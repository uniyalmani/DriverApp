from fastapi import FastAPI,WebSocket
from fastapi.middleware.cors import CORSMiddleware
from app.controllers.database_initializer import *
from app.routes import auth, location

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(auth.router)
app.include_router(location.router)

@app.get("/")
def read_root():

    return {"Hello": "World"}


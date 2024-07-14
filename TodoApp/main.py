from fastapi import FastAPI
from TodoApp.routers import auth
from TodoApp.routers import todos


app = FastAPI()

app.include_router(auth.router)
app.include_router(todos.router)

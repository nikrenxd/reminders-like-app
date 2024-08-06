from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.users.router import router as users_router
from src.collections.router import router as lists_router
from src.tasks.router import router as tasks_router


app = FastAPI()

origins = [
    "http://localhost:3000",
    "localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users_router)
app.include_router(lists_router)
app.include_router(tasks_router)

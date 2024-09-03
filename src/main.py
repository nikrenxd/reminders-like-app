from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from src.exceptions import AddException
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


@app.exception_handler(AddException)
async def add_exception_handler(request: Request, exc: AddException):
    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={"detail": "Can't create object"},
    )


app.include_router(users_router)
app.include_router(lists_router)
app.include_router(tasks_router)

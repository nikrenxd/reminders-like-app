from fastapi import APIRouter, status, Response

from src.users.service import UserService
from src.users.auth import get_hashed_password, create_jwt_token, authenticate_user
from src.users.schemas import SUserCreate

from src.exceptions import UserAlreadyExistsException, WrongCredentialsGivenException


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(body: SUserCreate) -> None:
    user = await UserService.get_one_by_fields(email=body.email)

    if user:
        raise UserAlreadyExistsException

    hashed_password = get_hashed_password(body.password)
    await UserService.add(
        email=body.email,
        password=hashed_password
    )


@router.post("/login")
async def login_user(response: Response, body: SUserCreate) -> dict[str, str]:
    user = await authenticate_user(body.email, body.password)

    if not user:
        raise WrongCredentialsGivenException

    access_token = create_jwt_token({"sub": str(user.id)})
    response.set_cookie("access_token", access_token, httponly=True)

    return {"access_token": access_token}


@router.post("/logout")
async def logout_user(response: Response) -> None:
    response.delete_cookie("access_token")

from fastapi import (
    APIRouter,
    Response,
    Request,
    Depends,
)
from app.models.users import (
    UserModel as User,
    OTPverify,
    RegisterUser,
    LoginUser,
)
from app.controllers.user import (
    UserController,
)
from app.utils.JWT import (
    check_token,
)
from app.middleware.user import Middleware as User_Middleware


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/send-otp")
async def send_otp(
    user: User,
    _: None = Depends(check_token),
):
    return await UserController.send_otp(user)


@router.post("/register")
async def register(user: RegisterUser, response: Response):
    return await UserController.register(user, response)


@router.post("/login")
async def login(user: LoginUser, response: Response):
    return await UserController.login(user, response)


@router.get("/me")
async def me(current_user=Depends(User_Middleware.me)):
    return current_user


@router.post("/verify-otp")
async def verify_otp(
    otp: OTPverify,
    response: Response,
    request: Request,
    _: None = Depends(check_token),
):
    return await UserController.verify_otp(
        otp,
        response,
        request,
    )


@router.get("/google/login")
async def google_login(
    request: Request,
):
    return await UserController.google_login(request)


@router.get("/google/callback")
async def google_callback(
    request: Request,
):
    return await UserController.google_callback(request)


@router.get("/github/login")
async def github_login(
    request: Request,
):
    return await UserController.github_login(request)


@router.get("/github/callback")
async def github_callback(
    request: Request,
):
    return await UserController.github_callback(request)


@router.post("/logout")
async def logout(response: Response, _: None = Depends(User_Middleware.me)):
    return await UserController.logout(response)

from fastapi import Depends, APIRouter, HTTPException, status
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from app.schemas.user import UserCreate, UserRead, Token
from app.use_cases.user_use_cases import UserUseCases, UserAlreadyExistsError, InvalidCredentialError
from app.dependencies import get_user_use_cases, get_current_user

router = APIRouter()
@router.post("/auth/register", status_code=201)
def register(user: UserCreate, use_case: UserUseCases=Depends(get_user_use_cases)) -> UserRead:
    try:
        user = use_case.register(user)
    except UserAlreadyExistsError as error:
        raise HTTPException(status_code=409, detail=error.detail)
    return user

@router.get("/auth/me")
def who_am_i(user: UserRead = Depends(get_current_user)) -> UserRead:
    return user
    

@router.post("/auth/login")
def login(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], use_case: UserUseCases=Depends(get_user_use_cases)) -> Token:
    try:
        token = use_case.login(email=form_data.username, password=form_data.password)
    except InvalidCredentialError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=error.detail, headers={"www-authenticate":"Bearer"})
    return Token(access_token=token, token_type="bearer")

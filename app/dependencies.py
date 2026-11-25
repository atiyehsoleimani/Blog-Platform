from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from app.database import SessionLocal, get_db
from app.contracts.user_repository import UserRepository
from app.use_cases.user_use_cases import UserUseCases, InvalidCredentialError, UserRead
from app.repository.sqlalchemy_user_repository import SqlAlchemyUserRepository
from app.repository.sqlalchemy_post_repository import SqlAlchemyPostRepository
from app.use_cases.post_use_cases import PostUseCases
from app.contracts.post_repository import PostRepository

def get_user_repository(session: SessionLocal=Depends(get_db)) -> UserRepository:
    return SqlAlchemyUserRepository(session)
    
def get_user_use_cases(repository: UserRepository=Depends(get_user_repository)) -> UserUseCases:
    return UserUseCases(repository)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")
def get_current_user(
        token: str=Depends(oauth2_scheme),
        use_cases: UserUseCases=Depends(get_user_use_cases)
) -> UserRead:
    try:
        return use_cases.get_current_user(token)
    except InvalidCredentialError:
        raise HTTPException(status_code=401, headers={"WWW-Authenticate": "Bearer"}, detail="Could not validate user's credential")

def get_post_repository(session: SessionLocal=Depends(get_db)) -> PostRepository:
    return SqlAlchemyPostRepository(session)

def get_post_use_cases(repository: PostRepository=Depends(get_post_repository), user_repository: UserRepository=Depends(get_user_repository)) -> PostUseCases:
    return PostUseCases(repo=repository, user_repo=user_repository)

from app.contracts.user_repository import UserRepository
from app.schemas.user import UserCreate, UserRead, UserInDB, Token
import app.security as security
class UserAlreadyExistsError(Exception):
    pass
class EmailAlreadyTakenError(UserAlreadyExistsError):
    detail = "Email already taken."

class UserNameAlreadyTakenError(UserAlreadyExistsError):
    detail = "Username already taken."

class InvalidCredentialError(Exception):
    detail = "Invalid credential error."
class UserUseCases:
    def __init__(self, repo: UserRepository):
        self.repo = repo

    def register(self, user: UserCreate) -> UserRead:
        user.email = user.email.lower()
        if self.repo.exists_by_email(user.email) is True:
            raise EmailAlreadyTakenError
        if self.repo.exists_by_username(user.username) is True:
            raise UserNameAlreadyTakenError
        hashed_pass = security.hash_password(user.password)
        return self.repo.add(user.email, user.username, hashed_pass)
        
    def login(self, email: str, password: str) -> str:
        email = email.lower()
        if self.repo.exists_by_email(email) is False:
            raise InvalidCredentialError 
        user: UserInDB=self.repo.get_by_email(email)
        if security.verify_password(password, user.hashed_password):
             return security.create_access_token(user.id)
        else:
            raise InvalidCredentialError 

    
    def get_current_user(self, token: str) -> UserRead:
        user_id = security.decode_access_token(token, security.ALGORITHM)
        if user_id is None:
            raise InvalidCredentialError
        user = self.repo.get_by_id(user_id)
        if user is None:
             raise InvalidCredentialError
        return user

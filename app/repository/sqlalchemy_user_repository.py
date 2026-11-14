from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import User
from app.contracts.user_repository import UserRepository
from app.schemas.user import UserInDB, UserRead


class SqlAlchemyUserRepository(UserRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, id: int) -> UserRead | None:
        session = self.session
        user = session.get(User, id)
        if user is not None:
            return UserRead.model_validate(user)
        else:
            return None

    def get_by_email(self, email: str) -> UserInDB | None:
        user = self.session.scalar(select(User).where(User.email==email))

        if user is not None:
            return UserInDB.model_validate(user)
        else:
            return None

    def get_by_username(self, username: str) -> UserRead | None:
        user = self.session.scalar(select(User).where(User.username==username))

        if user is not None:
            return UserRead.model_validate(user)
        else:
            return None

    def add(self, email: str, username: str, hashed_password: str) -> UserRead:
        session = self.session
        user = User(email=email, username=username, hashed_password=hashed_password)
        session.add(user)
        session.commit()
        session.refresh(user)
        return UserRead.model_validate(user)

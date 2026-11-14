from abc import ABC, abstractmethod
from app.schemas.user import UserRead, UserInDB


class UserRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> UserRead | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_email(self, email: str) -> UserInDB | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_username(self, username: str) -> UserRead | None:
        raise NotImplementedError

    @abstractmethod
    def add(self, email: str, username: str, hashed_password: str) -> UserRead:
        raise NotImplementedError

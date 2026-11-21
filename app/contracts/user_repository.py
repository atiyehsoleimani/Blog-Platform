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

    def exists_by_id(self, id: int) -> bool:
        return self.get_by_id(id) is not None

    def exists_by_username(self, username: str) -> bool:
        return self.get_by_username(username) is not None

    def exists_by_email(self, email: str) -> bool:
        return self.get_by_email(email) is not None

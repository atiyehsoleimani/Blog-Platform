from abc import ABC, abstractmethod
from app.schemas.post import PostRead


class PostRepository(ABC):
    @abstractmethod
    def get_by_id(self, id: int) -> PostRead | None:
        raise NotImplementedError

    @abstractmethod
    def get_by_author(self, author_id: int, limit: int, offset: int) -> list[PostRead]:
        raise NotImplementedError

    @abstractmethod
    def add(self, title: str, body: str, author_id: int) -> PostRead:
        raise NotImplementedError

    @abstractmethod
    def edit(self, post_id: int, title:str | None, body: str | None) -> PostRead:
        raise NotImplementedError
    @abstractmethod
    def delete(self, post_id: int):
        raise NotImplementedError


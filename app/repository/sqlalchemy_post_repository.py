from sqlalchemy import select
from sqlalchemy.orm import Session
from app.models import Post
from app.contracts.post_repository import PostRepository
from app.schemas.post import PostRead

class SqlAlchemyPostRepository(PostRepository):

    def __init__(self, session: Session):
        self.session = session

    def get_by_id(self, post_id: int) -> PostRead | None:
        
        post = self.session.get(Post, post_id)
        if post is not None:
            return PostRead.model_validate(post)
        else:
            return None

    def get_by_author(self, author_id: int, limit: int, offset: int) -> list[PostRead]:

        post_reads=[]
        posts = self.session.scalars(select(Post).where(Post.author_id == author_id).order_by(Post.created_at.desc(), Post.id.desc()).limit(limit=limit).offset(offset=offset)).all()
        for post in posts:
            post_reads.append(PostRead.model_validate(post))
        return post_reads   

    def add(self, title: str, body: str, author_id: int) -> PostRead:

        post = Post(title=title, body=body, author_id=author_id)
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return PostRead.model_validate(post)

    def edit(self, post_id: int, title: str | None, body: str | None) -> PostRead:
        post = self.session.get(Post, post_id)
        if body is not None:
            post.body = body
        if title is not None:
            post.title = title
        self.session.add(post)
        self.session.commit()
        self.session.refresh(post)
        return PostRead.model_validate(post)

    def delete(self, post_id: int):
        post = self.session.get(Post, post_id)
        self.session.delete(post)
        self.session.commit()
        
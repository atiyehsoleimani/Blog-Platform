from app.contracts.post_repository import PostRepository
from app.schemas.post import PostRead, PostCreate, PostUpdate
from app.contracts.user_repository import UserRepository
class PostNotFoundError(Exception):
    detail="Post Not Found"

class PostPermissionError(Exception):
    detail="You are not the author of this post"

class UserNotFoundError(Exception):
    detail="User not found"

class PostUseCases:
    def __init__(self, repo: PostRepository, user_repo: UserRepository):
        self.repo = repo
        self.user_repo = user_repo

    def add(self, post: PostCreate, author_id: int) -> PostRead:
        return self.repo.add(title=post.title, body=post.body, author_id=author_id)
        

    def edit(self, post_id: int, post_in: PostUpdate, current_user_id: int) -> PostRead:

        post = self.repo.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError
        if post.author_id != current_user_id:
            raise PostPermissionError
        
        return self.repo.edit(post_id, post_in.title, post_in.body)

    def delete(self, post_id: int, current_user_id: int):
        post = self.repo.get_by_id(post_id)

        if post is None:
            raise PostNotFoundError
        if post.author_id != current_user_id:
            raise PostPermissionError
        
        return self.repo.delete(post_id=post_id)
    

    def list_posts(self, author_id: int, limit: int, offset: int) -> list[PostRead]:
        if self.user_repo.exists_by_id(id=author_id) is False:
            raise UserNotFoundError
        return self.repo.get_by_author(author_id=author_id, limit=limit, offset=offset)

    def get_post(self, post_id: int) -> PostRead:
        post=self.repo.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError
        return post
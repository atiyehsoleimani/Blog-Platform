from app.contracts.post_repository import PostRepository
from app.schemas.post import PostRead, PostCreate, PostUpdate


class PostNotFoundError(Exception):
    detail="Post Not Found"

class PostPermissionError(Exception):
    detail="You do not delete/update permission on this post"

class PostUseCases:
    def __init__(self, repo):
        self.repo = repo

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
    

    def list_posts(self, author_id: int) -> list[PostRead]:
        return self.repo.get_by_author(author_id=author_id)

    def get_post(self, post_id: int) -> PostRead:
        post=self.repo.get_by_id(post_id)
        if post is None:
            raise PostNotFoundError
        return post
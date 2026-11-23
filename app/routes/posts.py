
from app.schemas.post import PostCreate, PostRead
from fastapi import Depends, APIRouter, HTTPException, status
from app.use_cases.post_use_cases import PostUseCases, PostNotFoundError, PostPermissionError
from app.dependencies import get_post_repository, get_post_use_cases, get_current_user
from app.schemas.user import UserRead


router = APIRouter()
@router.post("/posts", status_code=201)
def create_post(post: PostCreate, post_use_case: PostUseCases=Depends(get_post_use_cases), 
                user: UserRead = Depends(get_current_user)) -> PostRead:
    return post_use_case.add(post, user.id)

@router.get("/posts/{post_id}")
def get_post(post_id: int, post_use_case: PostUseCases=Depends(get_post_use_cases)) -> PostRead:
    try:
        post=post_use_case.get_post(post_id)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)
    return post
    

@router.get("/users/{user_id}/posts")
def list_posts(user_id: int, post_use_case: PostUseCases=Depends(get_post_use_cases)) -> list[PostRead]:
    return post_use_case.list_posts(author_id=user_id)

@router.delete("/posts/{post_id}", status_code=204)
def delete(post_id: int, post_use_case: PostUseCases=Depends(get_post_use_cases),
            current_user: UserRead=Depends(get_current_user)):
    try: 
        post_use_case.delete(post_id, current_user.id)
    except PostPermissionError as e :
        raise HTTPException(status_code=403, detail=e.detail)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)



    

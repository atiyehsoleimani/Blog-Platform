
from app.schemas.post import PostCreate, PostRead, PostUpdate
from fastapi import Depends, APIRouter, HTTPException, Query
from app.use_cases.post_use_cases import PostUseCases, PostNotFoundError, PostPermissionError, UserNotFoundError
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
def list_posts(user_id: int, post_use_case: PostUseCases=Depends(get_post_use_cases),
               limit: int = Query(default=5, ge=1, le=15),
                offset: int = Query(default=0, ge=0),
             ) -> list[PostRead]:
    try:
        return post_use_case.list_posts(author_id=user_id, limit=limit, offset=offset)
    except UserNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)


@router.patch("/posts/{post_id}")
def edit(post_id: int, post_in: PostUpdate, post_use_case: PostUseCases=Depends(get_post_use_cases),
            current_user: UserRead=Depends(get_current_user)) -> PostRead:
    
        try:
            post=post_use_case.edit(post_id=post_id, post_in=post_in, current_user_id=current_user.id)
            return post
        except PostPermissionError as e :
            raise HTTPException(status_code=403, detail=e.detail)
        except PostNotFoundError as e:
            raise HTTPException(status_code=404, detail=e.detail)
        

@router.delete("/posts/{post_id}", status_code=204)
def delete(post_id: int, post_use_case: PostUseCases=Depends(get_post_use_cases),
            current_user: UserRead=Depends(get_current_user)):
    try: 
        post_use_case.delete(post_id, current_user.id)
    except PostPermissionError as e :
        raise HTTPException(status_code=403, detail=e.detail)
    except PostNotFoundError as e:
        raise HTTPException(status_code=404, detail=e.detail)



    

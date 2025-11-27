from fastapi import APIRouter

exercise_router = APIRouter(prefix="/exercise", tags=["exercise"])


# @exercise_router.get('/')
# async def category_list(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @exercise_router.get('/{category_id}')
# async def category(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @exercise_router.post('/')
# async def create_category(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @exercise_router.get('/')
# async def update_category(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @exercise_router.get('/')
# async def delete_category(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @category_router.get('/')
# async def category_list(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @category_router.get('/{category_id}')
# async def category(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @category_router.post('/')
# async def create_category(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @category_router.get('/')
# async def update_category(session: Session = Depends(get_session)):
#     return {"message":"ola"}

# @category_router.get('/')
# async def delete_category(session: Session = Depends(get_session)):
#     return {"message":"ola"}
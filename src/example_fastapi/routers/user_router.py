from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status
from example_fastapi.dependencies.services import get_users_service
from example_fastapi.schemas.user import UserCreate, UserRead, UserUpdate
from example_fastapi.services.user_service import UserService
from example_fastapi.kafka import broker


router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/", response_model=list[UserRead])
async def get_users(
    user_service: UserService = Depends(get_users_service),
):
    return await user_service.get_users()


@router.post("/", status_code=status.HTTP_202_ACCEPTED)
async def create_user(
    user_data: UserCreate,
):
    await broker.publish(user_data.model_dump(), "create-user")
    return {"message": "User creation request received"}


@router.get("/{user_id}", response_model=UserRead)
async def get_user(
    user_id: UUID,
    user_service: UserService = Depends(get_users_service),
):
    user = await user_service.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.put("/{user_id}", response_model=UserRead)
async def update_user(
    user_id: UUID,
    user_data: UserUpdate,
    user_service: UserService = Depends(get_users_service),
):
    user = await user_service.update_user(user_id, user_data)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    return user


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: UUID,
    user_service: UserService = Depends(get_users_service),
):
    user = await user_service.delete_user(user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
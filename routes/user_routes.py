from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Order
from schemas import SignUpModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

user_router = APIRouter(prefix="/users", tags=["users"])


session = Session(bind=engine)


@user_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(Authorize: AuthJWT = Depends()):
    """
    ## Get all users registered in the database
    """
    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    users = session.query(User).all()

    return jsonable_encoder(users)


@user_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_specific_user(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Get a specific user by id
    This requires:
    ```
        id: int
    ```
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    user = session.query(User).filter(User.id == id).first()
    if user:
        response = {
            "message": "User found",
            "data": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "is_staff": user.is_staff,
                "is_active": user.is_active,
            },
        }
        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User of id:{id} not found"
    )


@user_router.get("/{id}/orders", status_code=status.HTTP_200_OK)
async def get_user_orders(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Gets all orders by a specific user by id
    This requires:
    ```
        id: int
    ```
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    user = session.query(User).filter(User.id == id).first()
    orders = session.query(Order).filter(Order.user_id == id).all()
    if user:
        response = {
            "message": "User Orders found",
            "data": {
                "user_id": user.id,
                "orders": orders,
            },
        }
        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User of id:{id} not found"
    )


@user_router.put("/{id}/update/", status_code=status.HTTP_201_CREATED)
async def update_user(id: int, user: SignUpModel, Authorize: AuthJWT = Depends()):
    """
    ## Updates a specific user's details
    This requires the following
    ```
        id: int
        username: str
        email: str
        password: str
        is_staff: bool
        is_active: bool
    ```
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        user_to_update = session.query(User).filter(User.id == id).first()

        user_to_update.username = user.username
        user_to_update.email = user.email
        user_to_update.password = user.password
        user_to_update.is_staff = user.is_staff
        user_to_update.is_active = user.is_active

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.with_traceback(),
            )

        response = {
            "message": "User Updated",
            "object": {
                "id": user_to_update.id,
                "username": user_to_update.username,
                "email": user_to_update.email,
                "is_staff": user_to_update.is_staff,
                "is_active": user_to_update.is_active,
            },
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )


@user_router.delete("/{id}/delete/", status_code=status.HTTP_200_OK)
async def delete_user(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Deletes a specific user from database
    This requires the following
    - id: int
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    if user.is_staff:
        user_to_delete = session.query(User).filter(User.id == id).first()

        try:
            session.delete(user_to_delete)
            session.commit()
        except Exception as e:
            session.rollback()
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.with_traceback(),
            )

        response = {
            "message": "Deleted",
            "object": {
                "id": user_to_delete.id,
                "username": user_to_delete.username,
                "email": user_to_delete.email,
            },
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )

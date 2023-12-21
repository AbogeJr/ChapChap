from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, FoodItem
from schemas import FoodItemModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

food_item_router = APIRouter(prefix="/food_item", tags=["food items"])


session = Session(bind=engine)


@food_item_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_food_items(Authorize: AuthJWT = Depends()):
    """
    ## Fetch all food items available in the database
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    food_items = session.query(FoodItem).all()

    return jsonable_encoder(food_items)


@food_item_router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_food_item(food_item: FoodItemModel, Authorize: AuthJWT = Depends()):
    """
    ## Add a new Food Item to database
    This requires the following
    - name: str
    - price: int
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
        # Check if the food item name is unique
        existing_food_item = (
            session.query(FoodItem).filter(FoodItem.name == food_item.name).first()
        )
        if existing_food_item:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Food item name must be unique",
            )

        new_food_item = FoodItem(name=food_item.name, price=food_item.price)

        try:
            session.add(new_food_item)
            session.commit()
        except Exception as e:
            session.rollback()
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.with_traceback(),
            )

        response = {
            "id": new_food_item.id,
            "name": new_food_item.name,
            "price": new_food_item.price,
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )


@food_item_router.get("/{id}")
async def get_specific_food_item(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Fetch a specific food item by id
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    food_item = session.query(FoodItem).filter(FoodItem.id == id).first()

    return jsonable_encoder(food_item)


@food_item_router.put("/{id}/update/", status_code=status.HTTP_202_ACCEPTED)
async def update_food_item(
    id: int, food_item: FoodItemModel, Authorize: AuthJWT = Depends()
):
    """
    ## Updates a specific Food item's details
    This requires the following
    - name: str
    - price: int
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
        food_item_to_update = session.query(FoodItem).filter(FoodItem.id == id).first()

        food_item_to_update.name = food_item.name
        food_item_to_update.price = food_item.price

        try:
            session.commit()
        except Exception as e:
            session.rollback()
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.with_traceback(),
            )

        response = {
            "id": food_item_to_update.id,
            "name": food_item_to_update.name,
            "price": food_item_to_update.price,
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )


@food_item_router.delete("/{id}/delete/", status_code=status.HTTP_200_OK)
async def delete_food_item(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Delete a specific Food item from database
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
        food_item_to_delete = session.query(FoodItem).filter(FoodItem.id == id).first()

        try:
            session.delete(food_item_to_delete)
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
                "id": food_item_to_delete.id,
                "name": food_item_to_delete.name,
                "price": food_item_to_delete.price,
            },
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )

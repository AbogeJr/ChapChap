from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, FoodItem
from schemas import FoodItemModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

food_item_router = APIRouter(prefix="/food_item", tags=["food items"])


session = Session(bind=engine)


@food_item_router.get("/")
async def get_all_food_items():
    """
    ## Gets all meals available in the database
    """
    meals = session.query(FoodItem).all()

    return jsonable_encoder(meals)


@food_item_router.post("/add", status_code=status.HTTP_201_CREATED)
async def create_food_item(meal: FoodItemModel, Authorize: AuthJWT = Depends()):
    """
    ## Create a new Meal
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
        # Check if the meal name is unique
        existing_meal = (
            session.query(FoodItem).filter(FoodItem.name == meal.name).first()
        )
        if existing_meal:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Meal name must be unique",
            )

        new_meal = FoodItem(name=meal.name, price=meal.price)

        session.add(new_meal)
        session.commit()

        response = {
            "id": new_meal.id,
            "name": new_meal.name,
            "price": new_meal.price,
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )


@food_item_router.get("/{id}")
async def get_specific_food_item(id: int):
    """
    ## Gets a specific meal by id
    """
    meal = session.query(FoodItem).filter(FoodItem.id == id).first()

    return jsonable_encoder(meal)


@food_item_router.put("/{id}/update/", status_code=status.HTTP_201_CREATED)
async def update_food_item(
    id: int, meal: FoodItemModel, Authorize: AuthJWT = Depends()
):
    """
    ## Updates a specific Meal's details
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
        meal_to_update = session.query(FoodItem).filter(FoodItem.id == id).first()

        meal_to_update.name = meal.name
        meal_to_update.price = meal.price

        session.commit()

        response = {
            "id": meal_to_update.id,
            "name": meal_to_update.name,
            "price": meal_to_update.price,
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )


@food_item_router.delete("/{id}/delete/", status_code=status.HTTP_201_CREATED)
async def delete_food_item(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Deletes a specific Meal's details
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
        meal_to_delete = session.query(FoodItem).filter(FoodItem.id == id).first()

        session.delete(meal_to_delete)

        session.commit()

        response = {
            "message": "Deleted",
            "object": {
                "id": meal_to_delete.id,
                "name": meal_to_delete.name,
                "price": meal_to_delete.price,
            },
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )

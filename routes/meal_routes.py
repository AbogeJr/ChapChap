from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models.order_model import Order
from models.user_model import User
from models.meal_model import Meal

from schemas import OrderModel, OrderStatusModel, MealModel
from database import Session, engine
from fastapi.encoders import jsonable_encoder

meal_router = APIRouter(prefix="/meals", tags=["meals"])


session = Session(bind=engine)


@meal_router.get("/meals")
async def get_all_meals(Authorize: AuthJWT = Depends()):
    """
    ## Gets all meals available in the database
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
        meals = session.query(Meal).all()

        return jsonable_encoder(meals)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )


@meal_router.post("/meal", status_code=status.HTTP_201_CREATED)
async def create_meal(meal: MealModel, session: Session = Depends()):
    """
    ## Create a new Meal
    This requires the following
    - name: str
    - price: int
    """

    # Check if the meal name is unique
    existing_meal = session.query(Meal).filter(Meal.name == meal.name).first()
    if existing_meal:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Meal name must be unique"
        )

    new_meal = Meal(name=meal.name, price=meal.price)

    session.add(new_meal)
    session.commit()

    response = {
        "id": new_meal.id,
        "name": new_meal.name,
        "price": new_meal.price,
    }

    return response

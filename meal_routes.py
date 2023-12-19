from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import User, Order, Meal
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
async def place_an_order(order: OrderModel, Authorize: AuthJWT = Depends()):
    """
    ## Adding a meal to the database
    This requires the following
    - name : string
    - price : integer

    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    new_order = Order(pizza_size=order.pizza_size, quantity=order.quantity)

    new_order.user = user

    session.add(new_order)

    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status,
    }

    return jsonable_encoder(response)

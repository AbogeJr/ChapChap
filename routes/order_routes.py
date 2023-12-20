from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models.user_model import User
from models.order_model import Order
from models.food_item_model import FoodItem
from schemas.order_schema import OrderCreate
from database import Session, engine
from fastapi.encoders import jsonable_encoder

order_router = APIRouter(prefix="/orders", tags=["order"])


session = Session(bind=engine)


@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_an_order(order: OrderCreate, Authorize: AuthJWT = Depends()):
    """
    ## Placing an Order
    This requires the following
    - quantity: integer
    - meal_ids: List[int]
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    current_user = Authorize.get_jwt_subject()

    user = session.query(User).filter(User.username == current_user).first()

    # Fetch food items by their IDs
    meals = session.query(FoodItem).filter(FoodItem.id.in_(order.meal_ids)).all()

    new_order = Order(pizza_size=order.pizza_size, quantity=order.quantity, meals=meals)

    new_order.user = user

    session.add(new_order)
    session.commit()

    response = {
        "pizza_size": new_order.pizza_size,
        "quantity": new_order.quantity,
        "id": new_order.id,
        "order_status": new_order.order_status,
        "meals": [{"id": meal.id, "name": meal.name} for meal in meals],
    }

    return response

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from fastapi_jwt_auth import AuthJWT
from models import OrderItem, Order, User
from schemas import OrderCreate, OrderItemCreate, OrderWithItems
from database import Session, engine
from fastapi.encoders import jsonable_encoder
from typing import List

order_router = APIRouter(prefix="/orders", tags=["orders"])


session = Session(bind=engine)


@order_router.get("/", status_code=status.HTTP_200_OK)
async def get_all_orders(Authorize: AuthJWT = Depends()):
    """
    ## Gets all orders made
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    orders = session.query(Order).all()

    return jsonable_encoder(orders)


@order_router.get("/{id}", status_code=status.HTTP_200_OK)
async def get_specific_order(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Gets a specific order by id
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    order = session.query(Order).filter(Order.id == id).first()
    if order:
        response = {
            "message": "Order found",
            "data": {
                "id": order.id,
                "order_status": order.order_status,
                "order_items": order.order_items,
                "user": order.user.username,
                "totals": order.total,
            },
        }
        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User of id:{id} not found"
    )


@order_router.post("/order", status_code=status.HTTP_201_CREATED)
async def place_an_order(
    order: OrderWithItems, userId: int, Authorize: AuthJWT = Depends()
):
    """
    ## Creates a new order with order items included:
    This requires:
    ```
        order_status: str
        order_items: List -> [
            {
                food_item_id: int
                quantity: int
            },
            {
                food_item_id: int
                quantity: int
            },
            ...
        ]
    ```
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    user = session.query(User).filter(User.id == userId).first()
    if user:
        # Create a new order

        new_order = Order()
        new_order.user_id = userId
        new_order.order_status = order.order_status
        try:
            session.add(new_order)
            session.commit()
        except Exception as e:
            session.rollback()
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.with_traceback(),
            )

        for item in order.order_items:
            new_order_item = OrderItem()
            new_order_item.order_id = new_order.id
            new_order_item.food_item_id = item.food_item_id
            new_order_item.quantity = item.quantity
            try:
                session.add(new_order_item)
                session.commit()
            except Exception as e:
                session.rollback()
                return HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.with_traceback(),
                )

            new_order_item.calculate_total
            new_order.calculate_total

        response = {
            "message": f"Order Created for user {userId}",
            "object": {
                "id": new_order.id,
                "order_status": new_order.order_status,
                "order_items": new_order.order_items,
                "user": new_order.user.username,
            },
        }

        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found"
    )


@order_router.put("/{id}/items", status_code=status.HTTP_201_CREATED)
async def add_order_items(
    id: int, order_items: List[OrderItemCreate], Authorize: AuthJWT = Depends()
):
    """
    ## Add order items to an order
    This requqires:
    ```
        id: int
        order_items: List -> [
            {
                food_item_id: int
                quantity: int
            },
            {
                food_item_id: int
                quantity: int
            },
            ...
        ]
    ```
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    order = session.query(Order).filter(Order.id == id).first()
    if order:
        for item in order_items:
            order_item_db = OrderItem(**item.dict())
            order_item_db.order_id = id
            try:
                session.add(order_item_db)
                session.commit()
            except Exception as e:
                session.rollback()
                return HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail=e.with_traceback(),
                )

            order_item_db.calculate_total
            order.calculate_total

        response = {"message": "Order items added", "data": order.order_items}
        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Order id:{id} not found"
    )


@order_router.get("/{id}/items", status_code=status.HTTP_200_OK)
async def get_specific_order_items(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Get order items within a specified order
    """

    try:
        Authorize.jwt_required()

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid Token"
        )

    order = session.query(Order).filter(Order.id == id).first()
    if order:
        response = {
            "message": "Order items found",
            "data": order.order_items,
        }
        return jsonable_encoder(response)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, detail=f"Order id:{id} not found"
    )


# @order_router.get("/{id}/items/{itemId}", status_code=status.HTTP_200_OK)
# async def get_specific_order_items_by_id(orderId: int, orderItemId: int):
#     """
#     ## Gets a specific order by id
#     """
#     order = session.query(Order).filter(Order.id == orderId).first()
#     if order:
#         order_item = (
#             session.query(OrderItem).filter(OrderItem.id == orderItemId).first()
#         )
#         if order_item:
#             response = {
#                 "message": "Order items found",
#                 "data": {
#                     "order": order_item.order,
#                     "food_item": order_item.food_item,
#                     "quantity": order_item.quantity,
#                     "total": order_item.total,
#                 },
#             }
#             return jsonable_encoder(response)

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail=f"Order id:{id} not found"
#     )


# @order_router.get("/{userId}/orders/", status_code=status.HTTP_200_OK)
# async def get_user_orders(userId: int):
#     """
#     ## Get all orders made by a specific user by id
#     This requires:
#     ```
#         id: int
#     ```
#     """
#     user = session.query(User).filter(User.id == userId).first()
#     if user:
#         response = {
#             "message": f"User Orders for < User: {user.username} >",
#             "data": {
#                 "user_id": user.id,
#                 "orders": user.orders,
#             },
#         }
#         return jsonable_encoder(response)

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail=f"User of id:{id} not found"
#     )


# @order_router.post("/create", status_code=status.HTTP_201_CREATED)
# async def place_an_order(
#     order: OrderCreate, userId: int, Authorize: AuthJWT = Depends()
# ):
#     user = session.query(User).filter(User.id == userId).first()
#     if user:
#         # Create a new order
#         new_order = Order(**order.dict())
#         new_order.user_id = userId
#         session.add(new_order)
#         session.commit()

#         response = {
#             "message": f"Order Created for user {userId}",
#             "object": {
#                 "id": new_order.id,
#                 "order_status": new_order.order_status,
#                 "user": new_order.user.username,
#             },
#         }

#         return jsonable_encoder(response)

#     raise HTTPException(
#         status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id:{id} not found"
#     )


@order_router.delete("/{id}/delete/", status_code=status.HTTP_200_OK)
async def delete_order(id: int, Authorize: AuthJWT = Depends()):
    """
    ## Deletes a specific order from database
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
        order_to_delete = session.query(Order).filter(Order.id == id).first()
        try:
            session.delete(order_to_delete)
            session.commit()
        except Exception as e:
            session.rollback()
            return HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=e.with_traceback(),
            )

        response = {
            "message": "Deleted Order",
            "object": {
                "id": order_to_delete.id,
                "status": order_to_delete.order_status,
                "user": order_to_delete.user.username,
            },
        }

        return response

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED, detail="You are not a superuser"
    )

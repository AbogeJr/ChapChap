from fastapi import APIRouter, FastAPI
from routes.auth_routes import auth_router
from routes.order_routes import order_router
from routes.food_item_routes import food_item_router
from routes.user_routes import user_router
from fastapi_jwt_auth import AuthJWT
from schemas.settings_schema import Settings
import inspect, re
from fastapi import FastAPI
from fastapi.routing import APIRoute
from fastapi.openapi.utils import get_openapi
from fastapi.encoders import jsonable_encoder

app = FastAPI()


def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="ChapChap: Fast Food Delivery API",
        version="1.0",
        description="An API for a Fast Food Delivery Services",
        routes=app.routes,
    )

    openapi_schema["components"]["securitySchemes"] = {
        "Bearer Auth": {
            "type": "apiKey",
            "in": "header",
            "name": "Authorization",
            "description": "Enter: **'Bearer &lt;JWT&gt;'**, where JWT is the access token",
        }
    }

    # Get all routes where jwt_optional() or jwt_required
    api_router = [route for route in app.routes if isinstance(route, APIRoute)]

    for route in api_router:
        path = getattr(route, "path")
        endpoint = getattr(route, "endpoint")
        methods = [method.lower() for method in getattr(route, "methods")]

        for method in methods:
            # access_token
            if (
                re.search("jwt_required", inspect.getsource(endpoint))
                or re.search("fresh_jwt_required", inspect.getsource(endpoint))
                or re.search("jwt_optional", inspect.getsource(endpoint))
            ):
                openapi_schema["paths"][path][method]["security"] = [
                    {"Bearer Auth": []}
                ]

    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


@AuthJWT.load_config
def get_config():
    return Settings()


base_router = APIRouter(tags=["welcome"])


@base_router.get("/")
async def welcome():
    """
    ## Welcome to ChapChap API

    """

    response = (
        "Welcome to ChapChap FastFood API 💥️. Check out the documetation at 👉️ http://localhost:8000/docs",
    )

    return response


app.include_router(base_router)
app.include_router(auth_router)
app.include_router(user_router)
app.include_router(order_router)
app.include_router(food_item_router)

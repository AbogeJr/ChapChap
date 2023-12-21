from pydantic import BaseModel


class Settings(BaseModel):
    authjwt_secret_key: str = "aboge"
    authjwt_access_token_expires: bool = False

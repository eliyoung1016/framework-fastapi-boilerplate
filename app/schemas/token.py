from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    refresh_token: str | None = None


class TokenPayload(BaseModel):
    sub: str | None = None
    exp: int | None = None
    refresh: bool | None = False

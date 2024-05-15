from pydantic import BaseModel
from itsdangerous import Signer

class User(BaseModel):
    id: int 
    name: str 
    username: str

class UserOut(BaseModel):
    data: User | None = None

class RenameIn(BaseModel):
    name: str 

class UpdateOut(BaseModel):
    ok: bool | None = None
    error: bool | None = None

SECRET_KEY = "mysterymysterymystery"
signer = Signer(SECRET_KEY)


def make_signed_cookie_token(id: str):
    signed_cookie = signer.sign(id)
    return signed_cookie.decode("utf-8")

def unsigned_cookie_token(signed_cookie: str):
    flatten_cookie = signer.unsign(signed_cookie)
    return int(flatten_cookie)

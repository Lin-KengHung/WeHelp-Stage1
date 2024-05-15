from fastapi import APIRouter, Cookie
from models import User, UserOut, RenameIn, UpdateOut, unsigned_cookie_token
from itsdangerous import BadSignature
from database import mycursor, mydb

router = APIRouter(
     prefix="/api", 
     tags=["Week7"]
)


@router.get("/member", response_model = UserOut)
async def name_query(username : str):
    mycursor.execute("SELECT id, name, username FROM member WHERE username = %s", (username,))
    user_info = mycursor.fetchone()
    if user_info != None:
        response = UserOut(data=User(id=user_info[0], name=user_info[1], username=user_info[2]))
    else:
        response = UserOut(data=None)
    response = response.model_dump()
    return response

@router.patch("/rename", response_model = UpdateOut, response_model_exclude_unset=True)
async def rename(new_name: RenameIn, cookie_token:  str  = Cookie()):
    try:
        user_id = unsigned_cookie_token(cookie_token)
        if user_id and new_name != "":
            sql = "UPDATE member SET name = %s WHERE id = %s"
            val = (new_name.name, user_id)
            mycursor.execute(sql, val)
            mydb.commit()
            response = UpdateOut(ok=True)
        else:
            response = UpdateOut(error=True)
        response = response.model_dump()
        return response
    except BadSignature:
        return  {"error": True}
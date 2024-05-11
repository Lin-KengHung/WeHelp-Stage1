from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from itsdangerous import Signer, BadSignature
import json

## test i am main##
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="123456",
  database="wehelp_week6"
)
mycursor = mydb.cursor()


# Endpotin part
@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={"header": "歡迎光臨，請輸入帳號密碼"})

@app.post("/signup")
async def signup(signupName: str = Form(default=None), signupUsername: str = Form(default=None), siguupPassword: str = Form(default="0000")):
    if (check_user(signupUsername)):
        message = "此帳號已經被註冊過了"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER)
    else:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        val = (signupName, signupUsername, siguupPassword)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
@app.post("/signin")
async def signin(response: Response, username: str = Form(), password: str = Form()):
    if (check_user(username, password)):
        id = check_user(username, password)
        response = RedirectResponse(url="/member",  status_code=status.HTTP_303_SEE_OTHER)
        token = make_signed_cookie_token(id)
        response.set_cookie(key="cookie_token", value=token, max_age=3600)
        return response
    else:
        message = "帳號或密碼輸入錯誤"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER) 
    
@app.get("/member")
async def show_member_page(request: Request, cookie_token : str = Cookie(default=None)):
    if (cookie_token != None):
        user_info = unsigned_cookie_token(cookie_token)

        # get messaage information
        mycursor.execute("SELECT message.id, message.content, member.id, member.name FROM message JOIN member ON message.member_id = member.id ORDER BY message.id")
        all_messages = mycursor.fetchall()
        process_messages = []
        for info in all_messages:
            info = list(info)
            if info[2] == user_info:
                info[2] = True
            else:
                info[2] = False
            process_messages.append(info)

        # get name
        mycursor.execute("SELECT name FROM member WHERE id = %s", (user_info,))
        name = mycursor.fetchone()[0]

        context = {"header": "這裡是會員頁面", "name": name + "，歡迎登入系統", "signout_url": "/signout", "logout": "登出系統", "board": process_messages}
        return templates.TemplateResponse(request=request, name="member.html", context=context)
    else:
        return RedirectResponse(url="/") 

@app.post("/createMessage")
async def createMessage(message: str = Form(default=None), cookie_token:  str  = Cookie()):
    try:
        user_info = unsigned_cookie_token(cookie_token)
        sql = "INSERT INTO message (member_id, content) VALUES (%s, %s)"
        val = (user_info, message)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse(url="/member",  status_code=status.HTTP_303_SEE_OTHER)
    except BadSignature:
        return {"message": "Invalid signature or expired cookie!"}
    
@app.post("/deleteMessage")
async def deleteMessage(data: str = Form(default=None), cookie_token:  str = Cookie()):
    try:
        user_info = unsigned_cookie_token(cookie_token)
        message_id = int(data)
        mycursor.execute("SELECT member_id FROM message WHERE id = %s", (message_id,))
        owner_id = mycursor.fetchone()[0]
        if owner_id == user_info:
            sql = "DELETE FROM message WHERE id =" + data
            mycursor.execute(sql)
            mydb.commit()
            return RedirectResponse(url="/member",  status_code=status.HTTP_303_SEE_OTHER)
        else :
            return RedirectResponse(url="./error?message=你不能亂刪別人留言", status_code=status.HTTP_303_SEE_OTHER)
    except BadSignature:
        return {"message": "Invalid signature or expired cookie!"}
  

@app.get("/error")
async def show_error_page(request: Request , message: str | None = "壞喔"):
    return templates.TemplateResponse(request=request, name="error.html", context={"header": "失敗頁面", "message": message, "signout_url": "/", "logout": "回去重登"})

@app.get("/signout")
async def signout(response: Response):
    response = RedirectResponse(url="/")
    response.delete_cookie(key="cookie_token")
    return response



def check_user(username, password=None):

    mycursor.execute("SELECT * FROM member WHERE username = %s" ,(username,))
    myresult= mycursor.fetchone()
    if myresult != None and  password == None:
        return True
    elif myresult != None and password == myresult[3]:
        return str(myresult[0])
    else:
        return False
    



SECRET_KEY = "mysterymysterymystery"
signer = Signer(SECRET_KEY)

def make_signed_cookie_token(id: str):
    signed_cookie = signer.sign(id)
    return signed_cookie.decode("utf-8")
    # cookie = {"id": id}
    # flatten_cookie = json.dumps(cookie).encode("utf-8")
    # signed_cookie = signer.sign(flatten_cookie)


def unsigned_cookie_token(signed_cookie: str):
    flatten_cookie = signer.unsign(signed_cookie)
    return int(flatten_cookie)
    # cookie = json.loads(flatten_cookie)
    # return cookie
    
    
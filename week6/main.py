from fastapi import FastAPI, Request, Form, Response, Cookie
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import mysql.connector
from itsdangerous import Signer, BadSignature
import json


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
async def signup(signupName: str = Form(default=None), signupUsername: str = Form(default=None), siguupPassword: str = Form(default=None)):
    print(signupName+ " "+ signupUsername + " " + siguupPassword)
    exist = check_user(signupUsername)
    if (exist):
        message = "此帳號已經被註冊過了"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER)
    else:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        val = (signupName, signupUsername, siguupPassword)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
@app.post("/signin")
async def signin(response: Response, username: str = Form(default=None), password: str = Form(default=None)):
    name = check_user(username)
    if name:
        response = RedirectResponse(url="/member",  status_code=status.HTTP_303_SEE_OTHER)
        token = make_signed_cookie_token(username, name)
        print(token)
        print(type(token))
        response.set_cookie(key="cookie_token", value=token.decode('utf-8'), max_age=3600)
        return response
    else:
        message = "帳號或密碼輸入錯誤"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER) 
    
@app.get("/member")
async def show_member_page(request: Request, cookie_token: str = Cookie(default=None)):
    if (cookie_token != None):
        user_info = unsigned_cookie_token(cookie_token.encode())
        mycursor.execute("SELECT * FROM message")
        all_messages = mycursor.fetchall()
        context = {"header": "這裡是會員頁面", "message": user_info["name"] + "，歡迎登入系統", "signout_url": "/signout", "logout": "登出系統", "board": all_messages, "username" : user_info["username"]}
        return templates.TemplateResponse(request=request, name="member.html", context=context)
    else:
        return RedirectResponse(url="/") 

@app.post("/createMessage")
async def createMessage(message: str = Form(default=None), cookie_token:  str  = Cookie()):
    try:
        user_info = unsigned_cookie_token(cookie_token)
        sql = "INSERT INTO message (name, username, content) VALUES (%s, %s, %s)"
        val = (user_info["name"], user_info["username"], message)
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
        mycursor.execute("SELECT username FROM message WHERE id = %s", (message_id,))
        query_username = mycursor.fetchone()[0]
        if query_username == user_info["username"]:
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
    print("i am here")
    return response



def check_user(username):
    mycursor.execute("SELECT * FROM member")
    myresult = mycursor.fetchall()
    for member in myresult:
        if username == member[1]:
            return member[0]
    return False

SECRET_KEY = "mysterymysterymystery"
signer = Signer(SECRET_KEY)

def make_signed_cookie_token(username, name):
    cookie = {"username": username, "name": name}
    flatten_cookie = json.dumps(cookie).encode('utf-8')
    signed_cookie = signer.sign(flatten_cookie)
    return signed_cookie

def unsigned_cookie_token(signed_cookie):
    flatten_cookie = signer.unsign(signed_cookie).decode('utf-8')
    cookie = json.loads(flatten_cookie)
    return cookie
    
from fastapi import FastAPI, Request, Form, Response, Cookie, status
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from itsdangerous import BadSignature
from routers import week7
from models import make_signed_cookie_token, unsigned_cookie_token
from database import mycursor, mydb



app = FastAPI(
    title="Week6 + Week7 assignmnet",
    version="1.0.0",
    summary="這裡是Summary",
    description="+ 這裡是支援markdown的description",
)

app.include_router(week7.router)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ----------------------------------------------------End point---------------------------------------------------------
@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request=request, name="home.html", context={"header": "歡迎光臨，請輸入帳號密碼"})

@app.post("/signup")
async def signup(signupName: str = Form(), signupUsername: str = Form(), siguupPassword: str = Form()):
    if (check_user(signupUsername)):
        message = "此帳號已經被註冊過了"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER)
    elif(signupName == "" or signupUsername == "" or siguupPassword == ""):
        message = "請勿有空值"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER)
    else:
        sql = "INSERT INTO member (name, username, password) VALUES (%s, %s, %s)"
        val = (signupName, signupUsername, siguupPassword)
        mycursor.execute(sql, val)
        mydb.commit()
        return RedirectResponse(url="/", status_code=status.HTTP_303_SEE_OTHER)
    
@app.post("/signin", response_class=RedirectResponse)
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
    
@app.get("/member", response_class=HTMLResponse)
async def show_member_page(request: Request, cookie_token : str = Cookie(default=None)):
    try:
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
    except BadSignature:
        return {"message": "Invalid signature or expired cookie!"}

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
        mycursor.execute("SELECT member_id FROM message WHERE id = %s", (data,))
        owner_id = mycursor.fetchone()[0]
        if owner_id == user_info:

            mycursor.execute("DELETE FROM message WHERE id = %s", (data,))
            mydb.commit()
            return RedirectResponse(url="/member",  status_code=status.HTTP_303_SEE_OTHER)
        else :
            return RedirectResponse(url="./error?message=你不能亂刪別人留言", status_code=status.HTTP_303_SEE_OTHER)
    except BadSignature:
        return {"message": "Invalid signature or expired cookie!"}
  

@app.get("/error", response_class=HTMLResponse)
async def show_error_page(request: Request , message: str | None = "壞喔"):
    return templates.TemplateResponse(request=request, name="error.html", context={"header": "失敗頁面", "message": message, "signout_url": "/", "logout": "回去重登"})

@app.get("/signout")
async def signout(response: Response):
    response = RedirectResponse(url="/")
    response.delete_cookie(key="cookie_token")
    return response

# -----------------------------------------------------------------------------------------------------------

def check_user(username, password=None):
    # global mydb, mycursor
    mycursor.execute("SELECT * FROM member WHERE username = %s" ,(username,))
    myresult= mycursor.fetchone()
    if myresult != None and  password == None:
        return True
    elif myresult != None and password == myresult[3]:
        return str(myresult[0])
    else:
        return False

    
    
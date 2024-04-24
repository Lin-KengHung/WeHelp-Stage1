from fastapi import FastAPI, Request, Form
from fastapi import FastAPI, status
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from starlette.middleware.sessions import SessionMiddleware



app = FastAPI()
app.add_middleware(SessionMiddleware, secret_key="some-random-string", max_age=None)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):

    return templates.TemplateResponse(request=request, name="home.html", context={"header": "歡迎光臨，請輸入帳號密碼"})

@app.post("/signin")
async def signin(request: Request, username: Annotated[str, Form()]=None, password: Annotated[str, Form()]=None):
    if username == "test" and password == "test":
        request.session["SIGNED-IN"] = True
        return RedirectResponse(url="/member", status_code=status.HTTP_303_SEE_OTHER)
    elif(username is None or password is None):
        message = "請輸入帳號密碼"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER) 
    else:
        message = "錯錯有餘！"
        return RedirectResponse(url="./error?message=" + message, status_code=status.HTTP_303_SEE_OTHER) 


@app.get("/member")
async def show_member_page(request: Request):
    login = request.session.get("SIGNED-IN", False)
    if (login):
        return templates.TemplateResponse(request=request, name="page2.html", context={"header": "這裡是會員頁面", "message": "成功登入啦！", "signout_url": "/signout", "logout": "登出系統"})
    else:
        return RedirectResponse(url="/")   

@app.get("/error")
async def show_error_page(request: Request , message: str | None = None):
    return templates.TemplateResponse(request=request, name="page2.html", context={"header": "登入失敗", "message": message, "signout_url": "/", "logout": "回去重登"})

@app.get("/signout")
async def signout(request: Request):
    request.session["SIGNED-IN"] = False
    return RedirectResponse(url="/")

@app.get("/square/{number}")
async def square(request: Request, number):
    return templates.TemplateResponse(request=request, name="page2.html", context={"header": "正整數平方計算的結果", "message": int(number)**2, "signout_url": "/", "logout": "返回首頁"})
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def landing(request: Request):
    return templates.TemplateResponse(request=request, name="login.html", context={"header": "歡迎光臨，請輸入帳號密碼"})

@app.post("/signin")
async def login(request: Request, username: Annotated[str, Form()]=None, password: Annotated[str, Form()]=None):
    if username == "test" and password == "test":
        return RedirectResponse("./member")
    elif(username is None or password is None):
        message = "請輸入帳號密碼"
        return RedirectResponse("./error?message=" + message) 
    else:
        message = "錯錯有餘！"
        return RedirectResponse("./error?message=" + message) 


@app.post("/member")
async def login(request: Request, response_class=HTMLResponse):
    return templates.TemplateResponse(request=request, name="member.html", context={"header": "這裡是會員頁面", "message": "成功登入啦！"})

@app.post("/error")
async def login(request: Request, response_class=HTMLResponse , message: str | None = None):
    
    return templates.TemplateResponse(request=request, name="error.html", context={"header": "登入失敗", "message": message})


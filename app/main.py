from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from app.db import SessionLocal
from app.models import Group, Server
from app.api import groups as groups_api, servers as servers_api  # 引入 API 路由
from app.monitor import start_monitor
app = FastAPI(title="ServerFailover Manager")

templates = Jinja2Templates(directory="app/templates")

# 注册 API 路由
app.include_router(groups_api.router)
app.include_router(servers_api.router)

# 获取数据库 session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    db = next(get_db())
    groups = db.query(Group).all()
    servers = db.query(Server).all()
    return templates.TemplateResponse("index.html", {"request": request, "groups": groups, "servers": servers})

@app.post("/add_group/")
def add_group(name: str = Form(...), script: str = Form(...)):
    db = next(get_db())
    group = Group(name=name, script=script)
    db.add(group)
    db.commit()
    return {"detail": "group added"}

@app.post("/add_server/")
def add_server(ip: str = Form(...), group_id: int = Form(...)):
    db = next(get_db())
    server = Server(ip=ip, group_id=group_id)
    db.add(server)
    db.commit()
    return {"detail": "server added"}

@app.on_event("startup")
def startup_event():
    # 启动后台监控线程，每 60 秒检查一次
    start_monitor(interval=60)
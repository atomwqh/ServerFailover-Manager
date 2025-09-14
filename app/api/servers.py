from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Server
from app.schemas import ServerCreate, ServerRead

router = APIRouter(prefix="/servers", tags=["servers"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=ServerRead)
def create_server(server: ServerCreate, db: Session = Depends(get_db)):
    db_server = Server(ip=server.ip, group_id=server.group_id, in_use=False)
    db.add(db_server)
    db.commit()
    db.refresh(db_server)
    return db_server

@router.get("/", response_model=list[ServerRead])
def list_servers(db: Session = Depends(get_db)):
    return db.query(Server).all()

@router.delete("/{server_id}")
def delete_server(server_id: int, db: Session = Depends(get_db)):
    server = db.query(Server).get(server_id)
    if not server:
        raise HTTPException(status_code=404, detail="Server not found")
    db.delete(server)
    db.commit()
    return {"message": "Deleted successfully"}

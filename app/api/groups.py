from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db import SessionLocal
from app.models import Group
from app.schemas import GroupCreate, GroupRead

router = APIRouter(prefix="/groups", tags=["groups"])

# 获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=GroupRead)
def create_group(group: GroupCreate, db: Session = Depends(get_db)):
    db_group = Group(name=group.name, script=group.script)
    db.add(db_group)
    db.commit()
    db.refresh(db_group)
    return db_group

@router.get("/", response_model=list[GroupRead])
def list_groups(db: Session = Depends(get_db)):
    return db.query(Group).all()

@router.delete("/{group_id}")
def delete_group(group_id: int, db: Session = Depends(get_db)):
    group = db.query(Group).get(group_id)
    if not group:
        raise HTTPException(status_code=404, detail="Group not found")
    db.delete(group)
    db.commit()
    return {"message": "Deleted successfully"}

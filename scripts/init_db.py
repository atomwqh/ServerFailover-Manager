from app.db import Base, engine
from app import models  # 确保导入，否则表不会注册到 Base.metadata

def init_db():
    print("正在创建数据库表，目标文件:", engine.url.database)
    Base.metadata.create_all(bind=engine)
    print("已创建表:", list(Base.metadata.tables.keys()))

if __name__ == "__main__":
    init_db()

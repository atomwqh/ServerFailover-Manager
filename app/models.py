from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db import Base


class Group(Base):
    __tablename__ = "groups"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    script = Column(String, nullable=False)

    servers = relationship("Server", back_populates="group")


class Server(Base):
    __tablename__ = "servers"
    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, unique=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))

    group = relationship("Group", back_populates="servers")

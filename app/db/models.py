from sqlalchemy import Column, Integer, String
from app.db.base import Base

class UserModel(Base):
    __tablename__ = "users"

    id = Column('id',Integer, primary_key=True, nullable=False, autoincrement=True)
    username = Column('username',String, unique=True, nullable=False)
    password = Column('password',String,nullable=False)
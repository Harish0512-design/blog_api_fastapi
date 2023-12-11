from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, LargeBinary, Boolean, TIMESTAMP, DateTime
from sqlalchemy.sql.expression import text
from app.database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    published = Column(Boolean, server_default='False')
    created_on = Column(TIMESTAMP(timezone=True), server_default=text('now()'))


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    email = Column(String(length=255), nullable=False)
    password = Column(String(length=255), nullable=False)
    created_on = Column(DateTime, default=datetime.utcnow)

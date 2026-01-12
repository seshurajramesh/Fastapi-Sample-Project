from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text,ForeignKey
from db import Base




class Votes(Base):
    __tablename__ = "votes"

    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"), primary_key=True)
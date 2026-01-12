from sqlalchemy import Column, Integer, String, Boolean, TIMESTAMP, text,ForeignKey
from sqlalchemy.orm import relationship
from db import Base
from models.users import User






class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable = False)
    title = Column(String, nullable = False)
    content = Column(String, nullable = False)
    published = Column(Boolean, nullable = False, server_default = 'TRUE')
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('NOW()'))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"), nullable = False)

    owner = relationship("User" , lazy="selectin")
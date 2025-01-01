from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Table
from sqlalchemy.orm import relationship
from database import Base
import datetime

class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    picture = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    user_id = Column(Integer, ForeignKey("users.id"))
    views = Column(Integer, default=0)

    user = relationship("User", back_populates="posts")
    likes = relationship("User", secondary="post_likes")
    hashtags = relationship("Hashtag", secondary="post_hashtags")

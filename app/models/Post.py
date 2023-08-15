from datetime import datetime
from app.db import Base
from .Vote import Vote
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, select
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from sqlalchemy.ext.hybrid import hybrid_property

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    post_url = Column(String(100), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'))
    created_at = Column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at = Column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
    user = relationship('User')
    comments = relationship('Comment', cascade='all,delete')
    # vote_count = column_property(
    #     select([func.count(Vote.id)]).where(Vote.post_id == id)
    # )
    votes = relationship('Vote', cascade='all,delete')

    def __repr__(self):
        return f'Post: {self.title}'
    # this is the way to do add  a column property in sqlalchemy 2.0 
    @hybrid_property
    def vote_count(self):
        return self._vote_count
    
    @vote_count.expression
    def _vote_count(cls):
        return select([func.count(Vote.id)]).where(Vote.post_id == cls.id).label('vote_count')
    
    
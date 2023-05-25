import datetime

from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, String, DateTime, Integer


Base = declarative_base()


class Quiz(Base):
    __tablename__ = 'quiz'
    id = Column(Integer, primary_key=True)
    question = Column(String, nullable=False)
    answer = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)
    pub_date = Column(DateTime, default=datetime.datetime.utcnow)

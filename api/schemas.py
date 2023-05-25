import datetime

from fastapi import HTTPException
from pydantic import BaseModel, validator

from settings import MAX_QUESTION_NUMS, MIN_QUESTION_NUMS


class GetQuestion(BaseModel):
    id: int
    question: str
    answer: str
    created_at: datetime.datetime


class QuestionsNum(BaseModel):
    questions_num: int

    @validator('questions_num')
    def validate_num(cls, value):
        if value not in range(MIN_QUESTION_NUMS, MAX_QUESTION_NUMS+1):
            raise HTTPException(
                status_code=422,
                detail='questions_num должен находится в промежутке от 1 до 10'
            )
        return value

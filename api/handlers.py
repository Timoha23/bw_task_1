from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from api.actions import create_new_questions, get_last_question
from api.schemas import GetQuestion, QuestionsNum
from db.session import get_db

quiz_router = APIRouter()


@quiz_router.post('/', response_model=GetQuestion | list, status_code=201)
async def add_quiz(
    questions: QuestionsNum,
    background_tasks: BackgroundTasks,
    session: AsyncSession = Depends(get_db)
):
    """
    Добавляем вопрос(ы) из квиза в БД
    """

    # получаем последний вопрос
    last_question = await get_last_question(session=session)
    # создаем новые вопросы и оборачиваем в background_tasks,
    # так как юзеру необязательно дожидаться пока все вопросы добавятся в БД
    background_tasks.add_task(
        create_new_questions,
        questions_num=questions.questions_num,
        session=session
    )
    if last_question is None:
        return []
    return GetQuestion(
        id=last_question.id,
        question=last_question.question,
        answer=last_question.answer,
        created_at=last_question.created_at,
    )

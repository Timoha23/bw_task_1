from datetime import datetime

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import Quiz
from external_api.quiz_api import get_questions


async def create_new_questions(
        questions_num: int,
        session: AsyncSession
) -> None:
    """
    Создаем новый(е) вопрос(ы) в БД
    """

    async with session.begin():
        questions = await get_questions(
            questions_num=questions_num
        )
        query = select(Quiz.id)
        res = await session.execute(query)

        # получаем id всех вопросов из БД
        questions_ids_in_db = [id[0] for id in res.fetchall()]
        questions_with_req_keys = []
        unique_questions = []

        # перебираем вопросы и если находим id вопроса в questions_ids_in_db,
        # либо в unique_questions, то получаем новый вопрос с jservice.io
        for question in questions:
            question_id = question.get('id')
            while (question_id in questions_ids_in_db or
                   question_id in unique_questions):
                question = await get_questions(questions_num=1)
                question_id = question[0].get('id')
            unique_questions.append(question)

        # заполняем список questions_with_req_keys с нужными нам данными
        for question in unique_questions:
            created_date = datetime.fromisoformat(
                question.get('created_at')[:-1]
            )
            quiz = {
                "id": question.get('id'),
                "question": question.get('question'),
                "answer": question.get('answer'),
                "created_at": created_date
            }
            questions_with_req_keys.append(quiz)
        # создаем объекты модели Quiz и помещаем их в список
        questions_to_db = [Quiz(**question) for question in
                           questions_with_req_keys]

        # добавляем данные объекты в БД
        session.add_all(questions_to_db)


async def get_last_question(session: AsyncSession) -> Quiz | None:
    """
    Получаем последний вопрос из БД
    """
    async with session.begin():
        query = select(Quiz).order_by(Quiz.pub_date.desc())
        res = await session.execute(query)
        questions = res.fetchone()
        if questions:
            return questions[0]

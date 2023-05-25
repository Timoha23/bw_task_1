from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from tests.conftest import get_questions


async def test_add_quiz(
        async_client: AsyncClient,
        db_session: AsyncSession
):
    """
    Тестирование добавления викторины
    """

    count_questions = 5

    questions = await get_questions(db_session=db_session)
    count_questions_before_good_request = len(questions)

    data = {"questions_num": count_questions}
    response_1 = await async_client.post("/", json=data)

    questions = await get_questions(db_session=db_session)
    count_questions_after_good_request = len(questions)

    last_question = questions[0][0]
    response_2 = await async_client.post("/", json=data)

    assert response_1.status_code == 201
    assert response_1.json() == []
    assert response_2.json()["id"] == last_question.id
    assert (count_questions_before_good_request + count_questions ==
            count_questions_after_good_request)


async def test_bad_add_quiz(
        async_client: AsyncClient,
        db_session: AsyncSession
):
    """
    Тестирование плохого запроса на добавление викторины
    """
    count_questions_less_then_need = 0
    count_questions_more_then_need = 11

    questions = await get_questions(db_session=db_session)
    count_questions_before_bad_request = len(questions)

    data = {"questions_num": count_questions_less_then_need}
    response_1 = await async_client.post("/", json=data)

    data = {"questions_num": count_questions_more_then_need}
    response_2 = await async_client.post("/", json=data)

    questions = await get_questions(db_session=db_session)
    count_questions_after_bad_request = len(questions)

    assert response_1.status_code == 422
    assert response_2.status_code == 422
    assert (count_questions_before_bad_request ==
            count_questions_after_bad_request)

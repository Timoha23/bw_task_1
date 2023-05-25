import aiohttp
from aiohttp.client_exceptions import ClientConnectionError
from fastapi import HTTPException

from settings import QUIZ_API_URL


async def get_questions(questions_num) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        url = QUIZ_API_URL + str(questions_num)
        try:
            async with session.get(url=url) as response:
                quiz_json = await response.json()
                return quiz_json
        except ClientConnectionError:
            raise HTTPException(
                status_code=503,
                detail="Сервис jservice.io не отвечает"
            )

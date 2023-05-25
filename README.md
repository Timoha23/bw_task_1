# Bewise Task 1
## Описание
___
Данный сервис предназначен для добавление вопросов для викторин в базу данных сервиса.

<details>
<summary>ТЗ проекта ↓</summary>

С помощью Docker (предпочтительно - docker-compose) развернуть образ с любой опенсорсной СУБД (предпочтительно - PostgreSQL). Предоставить все необходимые скрипты и конфигурационные (docker/compose) файлы для развертывания СУБД, а также инструкции для подключения к ней. Необходимо обеспечить сохранность данных при рестарте контейнера (то есть - использовать volume-ы для хранения файлов СУБД на хост-машине.
Реализовать на Python3 веб сервис (с помощью FastAPI или Flask, например), выполняющий следующие функции:
В сервисе должно быть реализован POST REST метод, принимающий на вход запросы с содержимым вида {"questions_num": integer}.
После получения запроса сервис, в свою очередь, запрашивает с публичного API (англоязычные вопросы для викторин) https://jservice.io/api/random?count=1 указанное в полученном запросе количество вопросов.
Далее, полученные ответы должны сохраняться в базе данных из п. 1, причем сохранена должна быть как минимум следующая информация (название колонок и типы данный можете выбрать сами, также можете добавлять свои колонки): 1. ID вопроса, 2. Текст вопроса, 3. Текст ответа, 4. - Дата создания вопроса. В случае, если в БД имеется такой же вопрос, к публичному API с викторинами должны выполняться дополнительные запросы до тех пор, пока не будет получен уникальный вопрос для викторины.
Ответом на запрос из п.2.a должен быть предыдущей сохранённый вопрос для викторины. В случае его отсутствия - пустой объект.
В репозитории с заданием должны быть предоставлены инструкции по сборке докер-образа с сервисом из п. 2., его настройке и запуску. А также пример запроса к POST API сервиса.
Желательно, если при выполнении задания вы будете использовать docker-compose, SQLAalchemy,  пользоваться аннотацией типов.

</details>

## Используемые технологии
___
![AppVeyor](https://img.shields.io/badge/Python-3.10.6-green)
![AppVeyor](https://img.shields.io/badge/FastAPI-0.95.2-9cf)
![AppVeyor](https://img.shields.io/badge/Alembic-1.11.0-9cf)
![AppVeyor](https://img.shields.io/badge/SQLAlchemy-2.0.13-9cf)
![AppVeyor](https://img.shields.io/badge/pytest-7.3.1-9cf)

![AppVeyor](https://img.shields.io/badge/Docker-20.10.21-green)
![AppVeyor](https://img.shields.io/badge/docker--compose-1.29.2-9cf)

![AppVeyor](https://img.shields.io/badge/Postgres-15.0-green)

## Запуск
___
###  Локально

1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/bewise_task_1.git
   ```

2. Создаем .env файл и заполняем в соответствии с примером (.env.example).
3. Создаем и активируем виртуальное окружение:
   ```bash
    python -m venv venv
   ```
   ```bash
   source venv/Scripts/activate
   ```
4. Устанавливаем зависимости:
    ```bash
    pip install -r -requirements.txt
    ```
5. Запускаем приложение:
   ```bash
   python main.py
   ```
###  Докер
1. Клонируем репозиторий:
   ```bash
   git clone https://github.com/Timoha23/bewise_task_1.git
   ```

2. Создаем .env файл и заполняем в соответствии с примером (.env.example).
3. Поднимаем контейнеры:
   ```bash
   docker-compose up -d --build
   ```
4. Создаем и накатываем миграции:
   ```bash
   docker exec -it app alembic revision --autogenerate -m 'comment'
   ```
   ```bash
   docker exec -it app alembic upgrade head
   ```

## Примеры запросов
___
1. Добавление вопроса
   * Endpoint: **host:port/**
   * Method: **POST**
   * Body: 
      ```json
      {
          "questions_num": 1
      }
        ```
   * Response: 
      ```json
      {
        "id": 1,
        "question": "<question>",
        "answer": "<answer>",
        "created_at": "<created_at>"
      }
      ```
   * Postman
     <details>
     <summary>Спойлер</summary>
      
     [![Пример запроса][1]][1]
      
     [1]: https://imageup.ru/img152/4351679/bw1.jpg
     </details>

## Внешние API
___
   * https://jservice.io

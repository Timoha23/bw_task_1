FROM python:3.10-alpine
WORKDIR /fastapi_app
COPY . .
RUN pip install -r requirements.txt --no-cache-dir
CMD ["python", "main.py"]
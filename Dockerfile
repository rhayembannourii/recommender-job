# app/Dockerfile
FROM python:3.9-slim

EXPOSE 8501

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app .

ENTRYPOINT ["streamlit", "run", "./main.py", "--server.port=8501", "--server.address=0.0.0.0"]
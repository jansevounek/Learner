# Use a lightweight Python image as the base
FROM python:3.9-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

RUN apt-get update && apt-get install -y \
    bash \
    && rm -rf /var/lib/apt/lists/*

COPY Learner_api /app/Learner_api

COPY Learner_scripts /app/Learner_scripts

COPY requirements.txt /app/

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5050

CMD ["python", "/app/Learner_api/run.py"]

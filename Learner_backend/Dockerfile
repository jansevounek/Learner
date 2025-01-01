FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY Learner_api /app/Learner_api
COPY Learner_scripts /app/Learner_scripts
COPY requirements.txt /app/requirements.txt

ENV PYTHONPATH=/app/Learner_api:/app/Learner_scripts:$PYTHONPATH

RUN pip install --no-cache-dir -r /app/requirements.txt

EXPOSE 5050

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5050", "wsgi:app"]


FROM python:3.10-slim

WORKDIR /app

COPY sprites/lighting_director/src/lighting_director ./lighting_director

COPY common/subscriber ./subscriber
COPY common/events ./events

COPY sprites/lighting_director/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-m", "lighting_director"]

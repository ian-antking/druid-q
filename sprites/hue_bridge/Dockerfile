FROM python:3.11-slim

WORKDIR /app

COPY sprites/hue_bridge/src/hue_bridge ./hue_bridge

COPY common/subscriber ./subscriber
COPY common/events ./events

COPY sprites/hue_bridge/requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-m", "hue_bridge"]

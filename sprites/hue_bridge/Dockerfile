FROM python:3.11-slim

WORKDIR /app

COPY ../../common/events/src/events /app/events
COPY ../../common/publisher/src/publisher /app/publisher

COPY ../../evokers/nfc/src/nfc /app/nfc
COPY ../../evokers/nfc/requirements.txt /app/requirements.txt
COPY ../../evokers/nfc/scenes.json /app/scenes.json

RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONPATH=/app

CMD ["python", "-m", "nfc"]

FROM python:3.8.3-alpine

WORKDIR /usr/src/weather-bot-proj/weatherbotapi

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

COPY . .

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

ENTRYPOINT ["/usr/src/weather-bot-proj/weatherbotapi/entrypoint.sh"]
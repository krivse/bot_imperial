FROM python:3.9.14-buster
ENV BOT_NAME=$BOT_NAME

WORKDIR /usr/src/app/"${BOT_NAME:-tg_bot}"

COPY requirements.txt /usr/src/app/"${BOT_NAME:-tg_bot}"
RUN pip install --upgrade pip && pip install -r /usr/src/app/"${BOT_NAME:-tg_bot}"/requirements.txt
COPY . /usr/src/app/"${BOT_NAME:-tg_bot}"

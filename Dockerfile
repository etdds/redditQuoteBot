FROM python:3.9-slim

RUN useradd --create-home --shell /bin/bash app_user
ENV PATH="${PATH}:/home/app_user/.local/bin"

COPY . /application

RUN chown -R app_user /application && \
    apt-get update && \
    apt-get install -y \
    git 
USER  app_user
RUN pip install --user /application

WORKDIR /home/app_user/run

CMD reddit_quote_bot.py
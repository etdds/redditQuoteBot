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
RUN pip install --user https://github.com/explosion/spacy-models/releases/download/en_core_web_md-3.4.1/en_core_web_md-3.4.1-py3-none-any.whl

WORKDIR /home/app_user/run

CMD reddit_quote_bot.py
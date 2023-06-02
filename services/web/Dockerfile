FROM python

WORKDIR /app

RUN addgroup --system app_user && adduser --system --group app_user
RUN apt-get update && apt-get install -yq --no-install-recommends -y

RUN chown -R app_user:app_user .

COPY ./config/requirements.txt ./config/requirements.txt
RUN python -m venv venv
RUN venv/bin/python -m pip install -U pip
RUN venv/bin/pip install -r config/requirements.txt

COPY ./logs /logs
COPY ./config ./config

COPY . .

RUN chmod 644 -R /logs
RUN chmod 666 ./config/.env

USER app_user

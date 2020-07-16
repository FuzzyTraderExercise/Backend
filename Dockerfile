FROM python:3.8.2-alpine


RUN apk update && \
    apk add --virtual build-deps gcc python3-dev musl-dev && \
    apk add postgresql-dev && \
    apk add netcat-openbsd && \
    apk add build-base


WORKDIR /src

COPY ./requirements.txt /src/requirements.txt
RUN pip install -r requirements.txt


COPY ./entrypoint.sh /src/entrypoint.sh
RUN chmod +x /src/entrypoint.sh


COPY . /src

CMD ["/src/entrypoint.sh"]
FROM python:3.10-alpine

RUN pip install --upgrade pip

COPY . .
RUN apk add nodejs npm
RUN npm install -g sass

RUN apk add --no-cache build-base
RUN apk add libsass-dev


RUN pip install -r requirements.txt

COPY ./entrypoint.sh /
ENTRYPOINT ["sh", "/entrypoint.sh"]

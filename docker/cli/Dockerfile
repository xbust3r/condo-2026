FROM python:3.9-bullseye

#RUN apk add --update --no-cache gcc unzip musl-dev g++ bash
RUN pip install --upgrade pip
RUN pip install fastapi
RUN pip install "uvicorn[standard]"

ADD resources /resources/
WORKDIR /resources/
RUN pip install -r ./requirements.txt

ARG USERNAME_LOCAL
ARG UID_LOCAL
ARG GID_LOCAL

RUN addgroup -g $GID_LOCAL $USERNAME_LOCAL || echo "This group already exists!"
#RUN adduser -u $UID_LOCAL -g $GID_LOCAL --disabled-password $USERNAME_LOCAL

WORKDIR /app

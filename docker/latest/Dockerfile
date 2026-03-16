ARG IMAGE_CLI
FROM $IMAGE_CLI

#RUN apk add --update --no-cache nginx
#RUN apk add --update --no-cache nginx

COPY ./entrypoint.sh /init/entrypoint.sh
RUN chmod +x /init/entrypoint.sh

WORKDIR /app

EXPOSE 7415

ENTRYPOINT ["sh", "/init/entrypoint.sh"]

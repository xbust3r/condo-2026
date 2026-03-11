ARG IMAGE_CLI
FROM $IMAGE_CLI

# Instalamos nginx usando apt-get
RUN apt-get update && \
    apt-get install -y nginx && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copia y otorga permisos al script de entrada
COPY ./entrypoint.sh /init/entrypoint.sh
RUN chmod +x /init/entrypoint.sh

# Establece el directorio de trabajo y expone el puerto 7415
WORKDIR /app
EXPOSE 7415

ENTRYPOINT ["sh", "/init/entrypoint.sh"]
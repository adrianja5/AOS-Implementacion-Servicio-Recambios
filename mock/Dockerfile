FROM stoplight/prism:4

COPY openapi-recambios /recambios
COPY nginx.conf /etc/nginx/nginx.conf
COPY entrypoints.sh entrypoints.sh


# Instalación de nginx y openrc
RUN apk add --no-cache nginx openrc && \
    mkdir -p /run/nginx && chown -R nginx:nginx /run/nginx/ && chmod 775 /run/nginx/ && \
    echo 'rc_provide="loopback net"' >> /etc/rc.conf && \
    openrc && touch /run/openrc/softlevel && \
    # Permisos para ejecución entrypoints.sh
    chmod 700 entrypoints.sh && \
    # Cambiar entrypoints.sh CRLF a LF por si se construye la imagen desde Windows
    dos2unix entrypoints.sh

EXPOSE 8080

ENTRYPOINT sh entrypoints.sh
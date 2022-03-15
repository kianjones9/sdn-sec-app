FROM mariadb:10.1

COPY config.sh /config.sh
RUN chmod +x /config.sh

COPY 01_schema.sql /docker-entrypoint-initdb.d
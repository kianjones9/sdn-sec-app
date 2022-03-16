FROM mariadb:10.1

COPY config.sh /config.sh
RUN chmod +x /config.sh

ADD 01_schema.sql /docker-entrypoint-initdb.d/
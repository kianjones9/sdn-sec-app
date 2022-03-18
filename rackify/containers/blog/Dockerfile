FROM m1k1o/blog

COPY config.sh /config.sh
RUN chmod +x /config.sh

ADD 01_schema.sql /docker-entrypoint-initdb.d/
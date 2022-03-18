FROM m1k1o/blog

RUN apt update && apt install -y iproute2

COPY config.sh /config.sh
RUN chmod +x /config.sh
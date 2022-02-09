
FROM ubuntu:18.04

RUN apt-get update && \
    apt-get install -y && \
    apt-get clean

CMD ["/bin/bash"]

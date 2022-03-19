FROM kianjones9/ovs:2.16_debian_5.8.0-63-generic

COPY config.sh /config.sh
RUN chmod +x /config.sh

COPY post-startup_config.sh /post-startup_config.sh
RUN chmod +x /post-startup_config.sh
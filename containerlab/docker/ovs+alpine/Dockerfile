FROM alpine:3.19

COPY ./utils/bin /usr/local/bin
COPY ./utils/start-all /usr/local/bin/start-all

RUN chmod +x /usr/local/bin/start_ovs_netdev && \
    chmod +x /usr/local/bin/start-all

RUN apk add openvswitch uuidgen iptables bash

ENV PATH="/usr/local/bin:${PATH}"

# ENTRYPOINT ["/sbin/tini", "--"]

CMD [ "start-all" ]
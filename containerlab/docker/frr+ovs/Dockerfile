FROM quay.io/frrouting/frr:10.1.1

COPY ./utils/bin /usr/local/bin
COPY ./utils/start-all /usr/local/bin/start-all

RUN chmod +x /usr/local/bin/start_ovs_netdev && \
    chmod +x /usr/local/bin/start-all

RUN apk add openvswitch uuidgen iptables

# debug mode
RUN apk add tcpdump ethtool

ENV PATH="/usr/local/bin:${PATH}"

ENTRYPOINT ["/sbin/tini", "--"]

CMD [ "start-all" ]
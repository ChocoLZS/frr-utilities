FROM python:3.10-slim AS base
FROM base AS prepare

RUN apt update \
    && apt install -y --no-install-recommends \
    wget unzip

WORKDIR /app

RUN wget -O ./ryu.zip "https://github.com/code-with-bgp-XD/ryu-patch/archive/refs/heads/master.zip" \
    && unzip ./ryu.zip \
    && mv ./ryu-patch-master ./ryu \
    && rm ./ryu.zip

FROM base AS runner

WORKDIR /app
COPY --from=prepare /app/ryu /app/ryu
RUN pip install /app/ryu
RUN pip install paramiko
RUN rm -rf /app/ryu

ADD bgpApp.py .
ADD bgpconf.py .

RUN apt update \
    && apt install -y --no-install-recommends \
    iproute2 iputils-ping openssh-client

# CMD ["ryu-manager", "bgpApp.py", "--bgp-app-config-file", "bgpconf.py"]
CMD ["/bin/bash"]

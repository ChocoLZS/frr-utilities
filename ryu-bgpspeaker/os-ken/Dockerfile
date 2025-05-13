FROM python:3.11-slim as prepare

RUN apt update && \
    apt install -y --no-install-recommends \
    git

WORKDIR /app

# 使用 git clone 替代 wget
RUN git clone https://github.com/openstack/os-ken.git && \
    cd os-ken && \
    git checkout 3.0.1

FROM python:3.11-slim as runner

WORKDIR /app

COPY --from=prepare /app/os-ken /app/os-ken

# 安装构建依赖
RUN apt update && \
    apt install -y --no-install-recommends \
    git && \
    pip install --upgrade pip && \
    pip install pbr && \
    cd /app/os-ken && \
    pip install .

# 清理
RUN rm -rf /app/os-ken && \
    apt remove -y git && \
    apt autoremove -y && \
    apt clean

# ADD bgpApp.py .
# ADD bgpconf.py .
# ADD start.sh .

RUN apt update \
    && apt install -y --no-install-recommends \
    iproute2 iputils-ping openssh-client

# CMD ["osken-manager", "bgpApp.py", "--bgp-app-config-file", "bgpconf.py"]
CMD ["bash"]

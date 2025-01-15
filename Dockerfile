FROM python:3.12-slim

WORKDIR /app/src

COPY . /app/src

#ENV http_proxy http://192.168.1.121:10809

# 更新 pip 并设置清华镜像源，然后安装依赖
RUN rm -rf /etc/apt/sources.list.d/* \
    && python -m pip install --upgrade pip -i https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple \
    && pip install --no-cache-dir -r requirements.txt \
    && rm -rf /root/.cache/pip

RUN echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm main contrib non-free non-free-firmware
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware" >> /etc/apt/sources.list && \
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-updates main contrib non-free non-free-firmware
    echo "deb https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware" >> /etc/apt/sources.list
# deb-src https://mirrors.tuna.tsinghua.edu.cn/debian/ bookworm-backports main contrib non-free non-free-firmware

RUN apt update
RUN apt install curl \
                -y
RUN apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# 暴露端口
# EXPOSE 5000

# 启动服务
CMD ["python", "main.py"]
FROM ubuntu:20.04

# 更新系统包
RUN apt-get update && apt-get install -y \
    python3 \
    python3-pip \
    python3-setuptools \
    build-essential \
    git \
    openjdk-8-jdk \
    unzip \
    zip \
    curl \
    wget \
    libc6-dev \
    libncurses5-dev \
    libgdbm-dev \
    libnss3-dev \
    libssl-dev \
    libreadline-dev \
    libffi-dev \
    libsqlite3-dev \
    libbz2-dev

# 设置环境变量
ENV ANDROID_HOME=/opt/android
ENV PATH=$PATH:$ANDROID_HOME/cmdline-tools/latest/bin:$ANDROID_HOME/platform-tools

# 创建工作目录
WORKDIR /app

# 安装Python依赖
RUN pip3 install --upgrade pip cython
RUN pip3 install buildozer

# 安装Android SDK
RUN mkdir -p $ANDROID_HOME && \
    cd /tmp && \
    wget https://dl.google.com/android/repository/commandlinetools-linux-7583922_latest.zip && \
    unzip commandlinetools-linux-7583922_latest.zip && \
    mkdir -p $ANDROID_HOME/cmdline-tools && \
    mv cmdline-tools $ANDROID_HOME/cmdline-tools/latest && \
    rm commandlinetools-linux-7583922_latest.zip

# 接受SDK许可证
RUN yes | sdkmanager --licenses || true

# 复制项目文件
COPY . /app

# 安装项目依赖
RUN buildozer android update

# 构建APK
RUN buildozer android debug

# 输出APK位置
RUN ls -la bin/
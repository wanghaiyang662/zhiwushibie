FROM ubuntu:22.04

# 国内网络优化：使用清华源
RUN apt-get update && apt-get install -y \
    openjdk-17-jdk \
    build-essential \
    libffi-dev \
    libssl-dev \
    autoconf \
    libtool \
    zipalign \
    libltdl-dev \
    pkg-config \
    zip \
    unzip \
    wget \
    curl \
    && rm -rf /var/lib/apt/lists/*

# 安装Python 3.9
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt-get update && apt-get install -y python3.9 python3.9-dev

# 安装Buildozer依赖
RUN pip3 install --upgrade pip
RUN pip3 install --index-url https://pypi.tuna.tsinghua.edu.cn/simple --trusted-host pypi.tuna.tsinghua.edu.cn \
    setuptools==65.5.0 \
    wheel \
    Cython==0.29.36 \
    buildozer==1.5.0

# 设置环境变量
ENV ANDROID_SDK_HOME /opt/android-sdk
ENV ANDROID_NDK_HOME /opt/android-ndk-r23b
ENV PATH "$PATH:$ANDROID_SDK_HOME/tools/bin:$ANDROID_SDK_HOME/platform-tools:$ANDROID_NDK_HOME"

# 创建SDK/NDK目录
RUN mkdir -p $ANDROID_SDK_HOME $ANDROID_NDK_HOME

# 下载Android SDK（国内加速）
RUN wget https://dl.google.com/android/repository/commandlinetools-linux-9477386_latest.zip -O sdk.zip && \
    unzip sdk.zip -d $ANDROID_SDK_HOME && \
    rm sdk.zip

# 下载NDK（23b版本，与buildozer.spec匹配）
RUN wget https://dl.google.com/android/repository/android-ndk-r23b-linux.zip -O ndk.zip && \
    unzip ndk.zip -d /opt && \
    rm ndk.zip

# 安装SDK组件（国内加速）
RUN yes | $ANDROID_SDK_HOME/tools/bin/sdkmanager "platform-tools" "platforms;android-34" "build-tools;34.0.0" "ndk;23.2.8568313"

# 设置默认SDK路径
RUN echo "sdk.dir=$ANDROID_SDK_HOME" > $ANDROID_SDK_HOME/local.properties

# 修复权限问题
RUN chown -R root:root /opt

# 默认工作目录
WORKDIR /app

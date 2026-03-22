#!/bin/bash

# Enhanced Quiz App - Android APK Build Script
# This script provides instructions for building the Android APK

echo "=== 永红林场动植物识别学习系统 APK 构建指南 ==="
echo
echo "由于当前环境限制，您需要在本地机器上完成APK构建。"
echo
echo "步骤 1: 准备本地开发环境"
echo "  - 安装Python 3.8+"
echo "  - 安装Buildozer: pip3 install buildozer cython"
echo
echo "步骤 2: 复制项目文件"
echo "  - 将以下文件复制到您的本地机器:"
echo "    * main.py"
echo "    * oss_sync.py"
echo "    * buildozer.spec"
echo "    * assets/ (如果有的话)"
echo
echo "步骤 3: 构建APK"
echo "  - 在项目根目录执行:"
echo "    buildozer android debug"
echo
echo "构建成功后，APK文件将在 bin/ 目录下生成。"
echo
echo "注意:"
echo "- 确保网络连接正常，因为构建过程需要下载大量依赖"
echo "- 初次构建可能需要较长时间，请耐心等待"
echo "- 如果遇到问题，请查看错误信息并根据提示解决"
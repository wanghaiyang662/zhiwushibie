[app]
# 基础应用配置
title = 永红林场动植物识别学习系统
package.name = enhancedquiz
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# 核心依赖（适配 GitHub Actions 编译环境）
requirements = python3,kivy==2.1.0,pillow,oss2,certifi,chardet,idna,urllib3,requests,crcmod,pycryptodome,aliyun-python-sdk-kms,aliyun-python-sdk-core,six,jmespath,cryptography,cffi,pycparser,charset_normalizer,pyjnius

# 界面配置
orientation = portrait
fullscreen = 0

# Android 核心配置（适配新版 Buildozer，移除弃用参数）
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.compileSdk = 31  # 替换旧的 android.sdk，适配新版 Buildozer
android.minapi = 21
android.ndk = 25b
android.release_artifact = apk
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = Theme.AppCompat.Light.NoActionBar
# 改回自动更新，让 Buildozer 自己安装缺失的构建工具
android.skip_update = False
# 关键：自动接受 SDK 许可（CI/CD 环境必须）
android.accept_sdk_license = True

# Python for Android 配置
p4a.branch = 2023.10.13  # 改用稳定版，不用开发版的master，避免bug
# 关键：增加构建超时时间（适配复杂依赖）
p4a.timeout = 1800

#
# OSX specific
#
osx.python_version = 3
osx.kivy_version = 2.1.0

[buildozer]
# CI/CD 环境专属配置
log_level = 2                # 详细日志，方便排查 Actions 构建问题
warn_on_root = 0             # 禁用 root 警告（GitHub Actions 以 root 运行）
# 关键：指定 Buildozer 缓存目录（复用 Actions 缓存）
build_dir = ./.buildozer
bin_dir = ./bin
# 关键：禁用交互式提示（CI/CD 环境必须）
disable_interactive = True

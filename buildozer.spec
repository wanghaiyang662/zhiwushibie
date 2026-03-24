[app]

# Application versioning
version = 1.0
package.name = enhancedquiz
package.domain = org.example

# Source code where the main file exists
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3,wav,ogg,jpeg,gif,bmp

# Application requirements
requirements = python3,kivy==2.1.0,pillow,oss2,certifi,chardet,idna,urllib3,requests,crcmod,pycryptodome,aliyun-python-sdk-kms,aliyun-python-sdk-core,six,jmespath,cryptography,cffi,pycparser,charset_normalizer,pyjnius,android

# Buildozer environment
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.minapi = 21
# 使用支持的NDK版本
android.ndk = 25b
android.sdk = 30
android.archs = armeabi-v7a,arm64-v8a

# Build settings
android.accept_sdk_license = True
p4a.branch = master

# Orientation - 必须是小写
orientation = portrait

# Title of application
title = 永红林场动植物识别学习系统

# Icon and splash
icon.filename = %(source.dir)s/icon.png
splash.filename = %(source.dir)s/splash.png

[buildozer]

# Logcat filter
log_level = 2

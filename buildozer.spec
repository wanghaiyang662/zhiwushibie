[app]
# 基础应用配置
title = 永红林场动植物识别学习系统
package.name = enhancedquiz
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
# 精简依赖：移除自动拉取的冗余项（如urllib3/chardet/idna，requests会自动带）
requirements = python3,kivy==2.1.0,pillow,oss2,requests,crcmod,pycryptodome,aliyun-python-sdk-kms,aliyun-python-sdk-core,six,jmespath,cryptography==36.0.2,cffi==1.15.1,pyjnius==1.6.1,setuptools==65.5.0
# 界面配置
orientation = portrait
fullscreen = 0
# Android 核心配置（严格匹配版本，适配p4a）
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 31
android.compileSdk = 31
android.minapi = 21
android.ndk = 25b  # 与环境变量ANDROID_NDK_HOME严格匹配
android.release_artifact = apk
android.entrypoint = org.kivy.android.PythonActivity
android.apptheme = Theme.AppCompat.Light.NoActionBar
android.skip_update = False
android.accept_sdk_license = True
# Python for Android 配置：固定分支，适配NDK25b
p4a.branch = master
p4a.timeout = 2400 # 延长编译超时
p4a.ndk_api = 21   # 与minapi一致，避免NDK编译冲突
# 禁用p4a的缓存清理，适配Actions缓存
p4a.no_clean = False

# OSX specific
osx.python_version = 3
osx.kivy_version = 2.1.0

[buildozer]
log_level = 2                # 详细日志，方便排查
warn_on_root = 0             # 禁用root警告（GitHub Actions默认root）
build_dir = ./.buildozer     # 项目内构建目录，适配Actions
bin_dir = ./bin              # APK输出目录
disable_interactive = True   # 禁用交互式提示（CI/CD必须）
android.logcat_format = long # 可选：更详细的Android日志

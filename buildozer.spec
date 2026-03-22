[app]
# 基础应用信息（简化命名，避免特殊字符）
title = TestApp
package.name = testapp
package.domain = org.test
version = 0.1

# 源码路径配置（仅保留核心文件）
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec
source.exclude_dirs = bin, .buildozer, .git
source.exclude_files = Makefile, .gitignore, README.md

# 核心依赖（仅保留Kivy+基础Python，无复杂库）
requirements = python3,kivy=2.1.0,pyjnius

# 界面配置
orientation = portrait
fullscreen = 0

# Android编译配置（适配新版Buildozer，无废弃字段）
android.api = 33
android.ndk = 25b
android.archs = arm64-v8a  # 替代废弃的android.arch
android.buildtools = 33.0.2
android.accept_sdk_license = True
android.permissions = INTERNET  # 仅保留基础网络权限
android.use_aapt2 = True
android.ndk_api = 33  # 让NDK API与android.api一致
android.minapi = 21  # 最低兼容安卓版本

# Buildozer全局配置
[buildozer]
log_level = 2  # 开启详细日志（方便排查）
warn_on_root = 1

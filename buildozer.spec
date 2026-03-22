[app]
title = 永红林场动植物识别
package.name = zhiwushibie
package.domain = org.wanghaiyang
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.include_dirs = assets/
source.exclude_exts = spec
source.exclude_dirs = bin, .buildozer, .git
source.exclude_files = Makefile, .gitignore, README.md

requirements = python3,kivy=2.1.0,pillow=9.2.0,oss2=2.18.4,certifi,chardet,idna,urllib3,requests,crcmod,pycryptodome,aliyun-python-sdk-kms,aliyun-python-sdk-core,six,jmespath,cryptography,cfi,pycparser,charset_normalizer,pyjnius

orientation = portrait
fullscreen = 0
android.api = 33
android.sdk = 24
android.ndk = 25b
android.arch = armeabi-v7a
android.buildtools = 30.0.3
android.use_aapt2 = True
android.permissions = INTERNET,ACCESS_NETWORK_STATE
android.meta_data =
android.entrypoint = main
android.apptheme = @android:style/Theme.Holo.Light
android.allow_backup = True
android.keyalias =
android.keypassword =
android.keystore =
android.keystorepassword =
android.ndk_path =
android.sdk_path =
android.ndk_version =
android.sdk_version =
android.buildtools_version =
android.use_androidx = False
android.enable_androidx = False

[buildozer]
log_level = 2
warn_on_root = 1

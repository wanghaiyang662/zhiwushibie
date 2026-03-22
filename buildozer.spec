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

requirements = python3,kivy=2.1.0,pillow=9.2.0,pyjnius

orientation = portrait
fullscreen = 0
android.api = 33
android.sdk = 33
android.ndk = 25b
android.arch = arm64-v8a
android.buildtools = 30.0.2
android.accept_sdk_license = True
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

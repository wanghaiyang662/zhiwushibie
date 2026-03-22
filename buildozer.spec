[app]
title = TestApp
package.name = testapp
package.domain = org.test
version = 0.1

source.dir = .
source.include_exts = py,png,jpg,kv,atlas
source.exclude_exts = spec
source.exclude_dirs = bin, .buildozer, .git
source.exclude_files = Makefile, .gitignore, README.md

requirements = python3,kivy=2.1.0,pyjnius

orientation = portrait
fullscreen = 0

android.api = 33
android.ndk = 25b
android.archs = arm64-v8a
android.buildtools = 33.0.2
android.accept_sdk_license = True
android.permissions = INTERNET
android.use_aapt2 = True
android.ndk_api = 33
android.minapi = 21

[buildozer]
log_level = 2
warn_on_root = 1

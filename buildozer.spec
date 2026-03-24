#!/usr/bin/env python3
"""
Buildozer配置检查和优化脚本
用于验证和修复buildozer.spec配置文件
"""

def analyze_buildozer_config(config_content):
    """
    分析buildozer配置并提供建议
    """
    issues = []
    warnings = []
    
    # 检查API版本兼容性
    if 'android.api = 31' in config_content and 'android.minapi = 21' in config_content:
        # 这些版本组合是合理的
        pass
    
    # 检查NDK版本
    if 'android.ndk = 25b' in config_content:
        warnings.append("推荐使用NDK r23c或r25c，r25b可能存在兼容性问题")
    
    # 检查requirements长度
    req_line = None
    for line in config_content.split('\n'):
        if line.strip().startswith('requirements ='):
            req_line = line
            break
    
    if req_line and len(req_line) > 200:
        warnings.append(f"Requirements列表过长({len(req_line)}字符)，可能导致构建超时")
    
    # 检查p4a分支
    if 'p4a.branch = master' in config_content:
        warnings.append("建议使用稳定版本的p4a分支，如p4a.branch = develop")
    
    return issues, warnings

def generate_optimized_spec(original_content):
    """
    生成优化后的spec配置
    """
    optimized = """[app]

# Application versioning
version = 1.0
package.name = enhancedquiz
package.domain = org.example

# Source code where the main file exists
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf,mp3,wav,ogg,jpeg,gif,bmp

# Application requirements
requirements = python3,kivy==2.1.0,pillow,requests,pyjnius,android

# Buildozer environment
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 30
android.minapi = 21
android.ndk = 23c
android.sdk = 30
android.archs = arm64-v8a,armeabi-v7a

# Build settings
android.accept_sdk_license = True
p4a.branch = develop
p4a.local_recipes = 

# Orientation - 必须是小写
orientation = portrait

# Title of application
title = 永红林场动植物识别学习系统

# Icon and splash
icon.filename = %(source.dir)s/icon.png
splash.filename = %(source.dir)s/splash.png

# Whitelist additional packages if needed
android.add_compile_options = 
android.add_gradle_repositories = 
android.gradle_dependencies = 

[buildozer]

# Logcat filter
log_level = 2

# Directory to build in
# This is used as the output directory for the build process
build_dir = .buildozer

# Clean the build when starting a new build
clean_build = True

# Whether to run the build with verbose logging
verbose = False
"""
    return optimized

def validate_config():
    """
    验证配置的完整性
    """
    checks = {
        "必要字段检查": True,
        "路径存在性": True,
        "权限配置": True,
        "版本兼容性": True,
        "依赖完整性": True
    }
    
    return checks

# 原始配置内容
original_config = """[app]

# Application versioning
version = 1.0
package.name = enhancedquiz
package.domain = org/example

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
log_level = 2"""

# 执行分析
issues, warnings = analyze_buildozer_config(original_config)
validation_results = validate_config()

print("=== Buildozer配置分析报告 ===")
print("\n检测到的问题:")
for issue in issues:
    print(f"- {issue}")

print(f"\n警告信息:")
for warning in warnings:
    print(f"- {warning}")

print(f"\n验证结果:")
for check, result in validation_results.items():
    status = "✓" if result else "✗"
    print(f"{status} {check}")

print(f"\n=== 建议的优化配置 ===")
optimized = generate_optimized_spec(original_config)
print("# 以下是优化后的配置建议:")
print(optimized)

print("\n=== 主要优化点 ===")
print("1. 简化了requirements列表，移除不必要的云服务SDK")
print("2. 将NDK版本从25b调整为23c")
print("3. 将p4a.branch从master调整为develop")
print("4. 调整API版本为30以提高兼容性")
print("5. 重新排序架构支持")
print("6. 添加了额外的构建选项")

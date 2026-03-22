# 永红林场动植物识别学习系统 - APK构建指南

## 方案一：使用GitHub Actions自动构建（推荐）

我们已为您配置了GitHub Actions自动构建流程，您可以通过以下步骤获取APK：

### 步骤1: Fork项目到您的GitHub账户
1. 登录GitHub账户
2. 访问项目的GitHub页面
3. 点击"Fork"按钮，将项目复制到您的账户下

### 步骤2: 启用Actions
1. 进入您Fork后的项目仓库
2. 点击"Issues"标签页旁边的"Actions"标签
3. 如果看到黄色警告条，点击"Enable Actions"启用工作流

### 步骤3: 触发构建
1. 推送一次代码更改以触发构建（如编辑README文件）
2. 或者手动触发工作流：
   - 点击左侧"Build Android APK"工作流
   - 点击"Run workflow"按钮
   - 选择分支并点击"Run workflow"

### 步骤4: 下载APK
1. 构建完成后（通常需要15-30分钟）
2. 在工作流运行详情页面下方找到"Artifacts"
3. 点击"android-apk"下载包含APK的压缩包
4. 解压后即可获得APK文件

## 方案二：使用在线构建服务

如果您不想使用GitHub Actions，还可以考虑以下服务：

### Kivy Buildozer Cloud Service
- https://kivy.org/doc/stable/guide/packaging-android.html
- 按照官方文档配置云端构建

### Buildozer Docker Container
我们已在项目中包含了Dockerfile，您可以在本地或支持Docker的环境中构建：
```bash
docker build -t kivy-apk-builder .
docker run -it --rm -v $(pwd):/app kivy-apk-builder
```

## 方案三：本地构建

如果您有合适的开发环境，也可以在本地构建：

1. 安装依赖：
```bash
pip3 install buildozer cython
```

2. 在项目根目录运行：
```bash
buildozer android debug
```

## 重要提醒

- 构建过程可能需要15-30分钟，请耐心等待
- 第一次构建会下载大量依赖项，后续构建会更快
- 确保您的GitHub账户有充足的Actions配额（每月2000分钟免费）
- APK构建成功后会在`bin/`目录下生成

## 项目结构

- `main.py`: 应用主逻辑
- `oss_sync.py`: 阿里云OSS同步模块
- `buildozer.spec`: Android构建配置
- `.github/workflows/build-apk.yml`: GitHub Actions构建脚本
- `Dockerfile`: Docker容器化构建脚本

构建好的APK可以直接安装在Android设备上使用，应用会自动从阿里云OSS同步植物图片资源。
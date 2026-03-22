# 永红林场动植物识别学习系统

这是一个基于Kivy的植物识别学习应用，可以从阿里云OSS同步植物图片并提供识别问答功能。

## 如何构建Android APK

此项目配置了GitHub Actions自动构建，您可以按照以下步骤获取APK：

### 方法1: 使用GitHub Actions（推荐）

1. Fork此仓库到您的GitHub账户
2. 推送代码到main分支，将会触发自动构建流程
3. 在Actions标签页中查看构建进度
4. 构建完成后，在Artifacts中下载APK文件

### 方法2: 本地构建

如果您想在本地构建：

1. 安装依赖：
   ```bash
   pip3 install buildozer cython
   ```

2. 初始化buildozer：
   ```bash
   buildozer init
   ```

3. 构建APK：
   ```bash
   buildozer android debug
   ```

构建成功的APK文件位于 `bin/` 目录下。

## 应用特性

- 从阿里云OSS同步植物图片
- 植物识别问答功能
- 答题统计和正确率计算
- 中文界面支持

## 技术栈

- Kivy: 跨平台GUI框架
- Python: 核心编程语言
- OSS2: 阿里云对象存储服务集成
- Buildozer: Android打包工具
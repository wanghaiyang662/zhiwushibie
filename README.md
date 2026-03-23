# 永红林场动植物识别学习系统

这是一个基于Kivy的植物识别学习应用，可以从阿里云OSS同步植物图片并提供识别问答功能。

## 功能特性

- 从阿里云OSS同步植物图片
- 植物识别问答功能
- 答题统计和正确率计算
- 中文界面支持
- 自动适配不同屏幕尺寸

## 构建说明

### 方法1: 使用GitHub Actions（推荐）

1. Fork此仓库到您的GitHub账户
2. 确保仓库设置中启用了Actions（Settings -> Actions -> General -> Workflow permissions）
3. 推送代码到main分支，将会自动触发构建流程
4. 或者手动触发：在Actions标签页点击"Build Android APK"，然后点击"Run workflow"
5. 在Actions的"Build Android APK"工作流中查看构建进度
6. 构建完成后，在Artifacts中下载APK文件

### 方法2: 本地构建

如果您想在本地构建：

1. 安装依赖：
   ```bash
   pip3 install buildozer cython
   ```

2. 在项目根目录运行：
   ```bash
   buildozer android debug
   ```

构建成功的APK文件位于 `bin/` 目录下。

## 项目结构

- `main.py` - 应用主逻辑
- `oss_sync.py` - 阿里云OSS同步模块
- `buildozer.spec` - Android构建配置
- `.github/workflows/build-apk.yml` - GitHub Actions构建脚本
- `requirements.txt` - Python依赖列表
- `assets/` - 资源文件目录

## 技术栈

- Kivy: 跨平台GUI框架
- Python: 核心编程语言
- OSS2: 阿里云对象存储服务集成
- Buildozer: Android打包工具
- GitHub Actions: CI/CD自动化构建

## 部署说明

应用首次运行时会从阿里云OSS下载所有植物图片，这可能需要一些时间，请耐心等待。下载完成后，应用会显示图片总数和同步统计信息。

应用需要网络权限以访问阿里云OSS，同时也需要存储权限以保存下载的图片。

## 故障排除

如果构建过程中出现问题：

1. 检查依赖是否完整安装
2. 确保有足够磁盘空间
3. 检查网络连接
4. 查看构建日志以获取详细错误信息

## 许可证

本项目仅供学习和参考使用。
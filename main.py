# 导入Kivy核心组件
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.core.window import Window

# 设置窗口背景（可选，仅增强可视化）
Window.clearcolor = (0.9, 0.9, 0.9, 1)

# 定义基础应用类
class MinimalTestApp(App):
    # 构建UI界面
    def build(self):
        # 创建布局容器
        layout = BoxLayout(orientation='vertical', padding=50, spacing=20)
        
        # 添加标题标签
        title_label = Label(
            text="构建成功！",
            font_size=40,
            color=(0.2, 0.5, 0.8, 1)
        )
        
        # 添加说明标签
        desc_label = Label(
            text="这是最简Kivy Demo，说明Buildozer编译流程正常",
            font_size=20,
            color=(0.3, 0.3, 0.3, 1)
        )
        
        # 将标签添加到布局
        layout.add_widget(title_label)
        layout.add_widget(desc_label)
        
        # 返回主布局
        return layout

# 程序入口
if __name__ == "__main__":
    MinimalTestApp().run()

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.image import Image
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.scrollview import ScrollView
from kivy.core.window import Window
from kivy.uix.behaviors import ButtonBehavior
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.graphics import Color, Rectangle
from kivy.core.text import LabelBase
import os
import sys
import random
import threading
from kivy.resources import resource_add_path, resource_find

# 尝试导入Android特定模块，不强制依赖
try:
    from android.storage import primary_external_storage_path
    ANDROID_STORAGE_AVAILABLE = True
except ImportError:
    ANDROID_STORAGE_AVAILABLE = False

try:
    from android import mActivity
    ANDROID_ACTIVITY_AVAILABLE = True
except ImportError:
    ANDROID_ACTIVITY_AVAILABLE = False

# 确保导入oss2模块
try:
    from oss_sync import sync_photos_from_oss, get_photo_list
    OSS_AVAILABLE = True
except ImportError:
    print("OSS模块不可用，使用本地图片")
    OSS_AVAILABLE = False

# 注册支持中文的字体
if sys.platform == 'win32':
    try:
        LabelBase.register(name='SimHei', fn_regular='C:\\Windows\\Fonts\\simhei.ttf')
    except:
        print("Windows字体加载失败，使用默认字体")
elif getattr(sys, 'platform') == 'linux' and 'ANDROID_DATA' in os.environ:
    # Android平台特殊处理
    try:
        from android.storage import primary_external_storage_path
        font_path = os.path.join(primary_external_storage_path(), 'simhei.ttf')
        if os.path.exists(font_path):
            LabelBase.register(name='SimHei', fn_regular=font_path)
        else:
            print("未找到中文字体，使用默认字体")
    except ImportError:
        print("Android模块不可用，使用默认字体")
    except Exception as e:
        print(f"加载中文字体失败: {e}")
else:
    # 其他平台
    try:
        # 尝试使用系统字体
        import platform
        if platform.system() == "Darwin":  # macOS
            LabelBase.register(name='SimHei', fn_regular='/System/Library/Fonts/PingFang.ttc')
        elif platform.system() == "Linux":  # Linux/Android
            # 尝试几个常见的中文字体路径
            font_paths = [
                '/system/fonts/DroidSansFallback.ttf',
                '/system/fonts/NotoSansCJK-Regular.ttc',
                '/system/fonts/NotoSansCJK-Bold.ttc'
            ]
            font_found = False
            for font_path in font_paths:
                if os.path.exists(font_path):
                    LabelBase.register(name='SimHei', fn_regular=font_path)
                    font_found = True
                    break
            if not font_found:
                print("未找到系统中文字体，使用默认字体")
    except Exception as e:
        print(f"注册中文字体时出错: {e}")

# 设置窗口大小和背景色
Window.size = (480, 800)
Window.clearcolor = (0.95, 0.95, 0.95, 1)

# 加载KV语言文件
Builder.load_string('''
<QuizScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 10
        spacing: 10
        
        # 标题栏
        BoxLayout:
            size_hint_y: None
            height: 80
            orientation: 'vertical'
            canvas.before:
                Color:
                    rgba: 0.18, 0.49, 0.19, 1  # 深绿色
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                text: '周至县国有永红生态林场'
                font_size: '18sp'
                color: 1, 1, 1, 1
                bold: True
                font_name: 'SimHei'
                size_hint_y: 0.5
            Label:
                text: '野生植物识别学习系统'
                font_size: '18sp'
                color: 1, 1, 1, 1
                bold: True
                font_name: 'SimHei'
                size_hint_y: 0.5
        
        # 图片显示区域
        ScrollView:
            size_hint_y: 0.5
            Image:
                id: image_display
                source: ''
                size_hint: None, None
                size: self.texture_size
                allow_stretch: True
                keep_ratio: True
                pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        # 选项区域
        GridLayout:
            id: options_grid
            cols: 2
            spacing: 10
            size_hint_y: 0.3
        
        # 统计信息区域
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 50
            padding: 10
            canvas.before:
                Color:
                    rgba: 0.9, 0.9, 0.9, 1
                Rectangle:
                    pos: self.pos
                    size: self.size
            Label:
                id: stats_label
                text: '正确: 0 | 错误: 0 | 正确率: 0%'
                font_size: '16sp'
                color: 0, 0, 0, 1
                font_name: 'SimHei'
        
        # 控制按钮区域
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: 60
            spacing: 10
            Button:
                id: submit_btn
                text: '确认提交'
                font_size: '18sp'
                background_color: 0.3, 0.3, 0.3, 1
                disabled: True
                font_name: 'SimHei'
                on_press: root.check_answer()
            Button:
                text: '下一题'
                font_size: '18sp'
                background_color: 0.18, 0.49, 0.19, 1
                font_name: 'SimHei'
                on_press: root.new_question()

<ResultScreen>:
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        Label:
            text: '答题完成'
            font_size: '24sp'
            bold: True
            font_name: 'SimHei'
        Label:
            id: final_stats
            text: ''
            font_size: '20sp'
            halign: 'center'
            valign: 'middle'
            size_hint_y: 0.5
            text_size: self.size
            font_name: 'SimHei'
        Button:
            text: '重新开始'
            font_size: '20sp'
            background_color: 0.18, 0.49, 0.19, 1
            font_name: 'SimHei'
            on_press: root.restart_game()
        Button:
            text: '退出'
            font_size: '20sp'
            background_color: 0.7, 0.2, 0.2, 1
            font_name: 'SimHei'
            on_press: app.stop()
''')

class QuizScreen(Screen):
    def __init__(self, **kwargs):
        super(QuizScreen, self).__init__(**kwargs)
        self.photo_dir = None
        self.all_photos = []
        self.used_photos = set()
        self.answer_bank = []
        self.current_answer = ""
        self.correct = 0
        self.wrong = 0
        self.selected_option = None
        self.sync_complete = False
        
        Clock.schedule_once(self.initialize_app, 0)
    
    def initialize_app(self, dt):
        print("正在初始化应用...")
        self.setup_photo_directory()
        if OSS_AVAILABLE:
            Clock.schedule_once(self.sync_and_load_photos, 1)
        else:
            Clock.schedule_once(self.load_photos, 1)
        self.new_question()
    
    def setup_photo_directory(self):
        """设置照片目录"""
        if hasattr(sys, '_MEIPASS'):
            base_path = os.path.join(sys._MEIPASS, 'assets', 'animal_photos')
        elif sys.platform == 'android':
            try:
                if ANDROID_STORAGE_AVAILABLE:
                    app_name = 'enhancedquiz'
                    base_path = os.path.join(primary_external_storage_path(), app_name, 'assets', 'animal_photos')
                    if not os.path.exists(base_path):
                        os.makedirs(base_path, exist_ok=True)
                else:
                    # 如果Android模块不可用，使用临时目录
                    base_path = os.path.join('/tmp', 'animal_photos')
                    if not os.path.exists(base_path):
                        os.makedirs(base_path, exist_ok=True)
            except Exception as e:
                print(f"获取Android存储路径失败: {e}")
                base_path = os.path.join('/tmp', 'animal_photos')
                if not os.path.exists(base_path):
                    os.makedirs(base_path, exist_ok=True)
        else:
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'assets', 'animal_photos')
        
        if not os.path.exists(base_path):
            os.makedirs(base_path, exist_ok=True)
        
        self.photo_dir = base_path
        print(f"照片目录设置为: {self.photo_dir}")
    
    def sync_and_load_photos(self, dt):
        print("正在从阿里云OSS同步图片...")
        try:
            sync_photos_from_oss()
            self.sync_complete = True
            print("图片同步完成！")
        except Exception as e:
            print(f"图片同步失败: {e}")
        
        self.load_photos()
    
    def load_photos(self, dt=None):
        """加载照片文件"""
        if not self.photo_dir:
            print("照片目录未设置")
            return
        
        valid_ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
        try:
            files = [f for f in os.listdir(self.photo_dir) 
                    if f.lower().endswith(valid_ext)]
            
            if len(files) == 0:
                print("没有找到照片文件！")
                # 如果没有找到图片，创建占位符
                placeholder_img = os.path.join(self.photo_dir, 'placeholder.png')
                if not os.path.exists(placeholder_img):
                    # 创建一个简单的占位图片（实际开发中应使用真实的图片）
                    pass
                return
                
            if len(files) < 4:
                print("需要至少4张照片！")
                return
                
            self.answer_bank = [os.path.splitext(f)[0].split('.')[0] for f in files]
            self.all_photos = [os.path.join(self.photo_dir, f) for f in files]
            
            print(f"加载了 {len(self.all_photos)} 张照片")
            
        except Exception as e:
            print(f"加载照片失败：{e}")
    
    def new_question(self, *args):
        if not self.all_photos:
            print("没有可用的照片，请确保 assets/animal_photos 目录中有照片文件")
            return
        
        if len(self.used_photos) >= len(self.all_photos):
            self.show_final_result()
            return
        
        self.selected_option = None
        self.ids.submit_btn.disabled = True
        self.ids.submit_btn.background_color = 0.3, 0.3, 0.3, 1
        
        options_grid = self.ids.options_grid
        options_grid.clear_widgets()
        
        available = [p for p in self.all_photos if p not in self.used_photos]
        if not available:
            self.show_final_result()
            return
            
        photo_path = random.choice(available)
        self.used_photos.add(photo_path)
        
        self.ids.image_display.source = photo_path
        self.ids.image_display.reload()  # 确保图片更新
        
        correct = os.path.splitext(os.path.basename(photo_path))[0].split('.')[0]
        wrongs = [a for a in self.answer_bank if a != correct]
        
        if len(wrongs) < 3:
            # 如果错误选项不足，重复添加
            while len(wrongs) < 3:
                wrongs.append(random.choice(self.answer_bank))
        
        selected_wrong = random.sample(wrongs, 3) if len(wrongs) >= 3 else wrongs
        
        options = [correct] + selected_wrong
        random.shuffle(options)
        
        for option in options:
            btn = Button(
                text=option,
                font_size='22sp',
                background_color=(0.18, 0.49, 0.19, 1),
                font_name='SimHei',
                on_press=lambda instance, opt=option: self.select_option(instance, opt)
            )
            options_grid.add_widget(btn)
        
        self.current_answer = correct
        self.update_stats()
    
    def select_option(self, instance, option):
        for child in self.ids.options_grid.children:
            child.background_color = (0.18, 0.49, 0.19, 1)
        
        instance.background_color = (0.3, 0.7, 0.3, 1)
        self.selected_option = option
        
        self.ids.submit_btn.disabled = False
        self.ids.submit_btn.background_color = (0.2, 0.6, 0.2, 1)
    
    def check_answer(self):
        if not self.selected_option:
            return
        
        if self.selected_option == self.current_answer:
            self.correct += 1
            self.show_feedback("正确！", "green")
        else:
            self.wrong += 1
            self.show_feedback(f"错误！正确答案是：{self.current_answer}", "red")
        
        self.update_stats()
        
        Clock.schedule_once(lambda dt: self.new_question(), 2)
    
    def show_feedback(self, message, color):
        feedback = Label(
            text=message,
            font_size='24sp',
            color=(1, 1, 1, 1) if color == "green" else (1, 1, 1, 1),
            size_hint=(None, None),
            size=(300, 100),
            pos_hint={'center_x': 0.5, 'center_y': 0.5},
            font_name='SimHei'
        )
        
        feedback.canvas.before.clear()
        with feedback.canvas.before:
            Color(0.2, 0.6, 0.2, 0.9) if color == "green" else Color(0.8, 0.2, 0.2, 0.9)
            Rectangle(pos=feedback.pos, size=feedback.size)
        
        self.add_widget(feedback)
        
        Clock.schedule_once(lambda dt: self.remove_widget(feedback), 2)
    
    def update_stats(self):
        total = self.correct + self.wrong
        accuracy = (self.correct / total * 100) if total > 0 else 0
        self.ids.stats_label.text = f'正确: {self.correct} | 错误: {self.wrong} | 正确率: {accuracy:.1f}%'
    
    def show_final_result(self):
        total = self.correct + self.wrong
        accuracy = (self.correct / total * 100) if total > 0 else 0
        
        if self.manager:
            result_screen = self.manager.get_screen('result')
            result_screen.ids.final_stats.text = f"最终统计：\n\n正确：{self.correct}\n错误：{self.wrong}\n正确率：{accuracy:.1f}%"
            self.manager.current = 'result'
        else:
            print(f"最终统计：\n正确：{self.correct}\n错误：{self.wrong}\n正确率：{accuracy:.1f}%")

class ResultScreen(Screen):
    def restart_game(self):
        quiz_screen = self.manager.get_screen('quiz')
        
        quiz_screen.used_photos.clear()
        quiz_screen.correct = 0
        quiz_screen.wrong = 0
        quiz_screen.selected_option = None
        
        quiz_screen.new_question()
        
        self.manager.current = 'quiz'

class QuizApp(App):
    def build(self):
        sm = ScreenManager()
        
        sm.add_widget(QuizScreen(name='quiz'))
        sm.add_widget(ResultScreen(name='result'))
        
        return sm

if __name__ == '__main__':
    import sys
    
    if hasattr(sys, '_MEIPASS'):
        resource_add_path(os.path.join(sys._MEIPASS))
    
    QuizApp().run()

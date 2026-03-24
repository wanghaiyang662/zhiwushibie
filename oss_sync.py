import os
import hashlib
from pathlib import Path
import sys

# 尝试导入oss2，如果不可用则提供模拟功能
try:
    import oss2
    OSS_AVAILABLE = True
except ImportError:
    print("oss2模块不可用，使用模拟功能")
    OSS_AVAILABLE = False
    # 模拟oss2的功能
    class MockAuth:
        def __init__(self, *args, **kwargs):
            pass
    class MockBucket:
        def __init__(self, *args, **kwargs):
            pass
        def get_object_to_file(self, *args, **kwargs):
            pass
        def head_object(self, *args, **kwargs):
            class MockMeta:
                content_length = 0
            return MockMeta()
    class MockObjectIterator:
        def __init__(self, *args, **kwargs):
            pass
        def __iter__(self):
            return iter([])
    oss2 = type('MockOss2', (), {
        'Auth': MockAuth,
        'Bucket': MockBucket,
        'ObjectIterator': MockObjectIterator
    })()

# 从环境变量或配置文件获取OSS配置
ACCESS_KEY_ID = os.getenv("ALIYUN_ACCESS_KEY_ID", "YOUR_ACCESS_KEY_ID")
ACCESS_KEY_SECRET = os.getenv("ALIYUN_ACCESS_KEY_SECRET", "YOUR_ACCESS_KEY_SECRET")
ENDPOINT = os.getenv("OSS_ENDPOINT", "oss-cn-beijing.aliyuncs.com")
BUCKET_NAME = os.getenv("OSS_BUCKET_NAME", "dongzhiwushibie")
OSS_FOLDER = os.getenv("OSS_FOLDER", "植物识别学习图片/")

def get_local_photo_dir():
    """获取本地照片存储目录"""
    if hasattr(sys, '_MEIPASS'):
        base_path = os.path.join(sys._MEIPASS, 'assets', 'animal_photos')
    elif getattr(sys, 'platform') == 'linux' and 'ANDROID_DATA' in os.environ:
        try:
            from android.storage import primary_external_storage_path
            app_name = 'enhancedquiz'
            base_path = os.path.join(primary_external_storage_path(), app_name, 'assets', 'animal_photos')
            if not os.path.exists(base_path):
                os.makedirs(base_path, exist_ok=True)
        except ImportError:
            print("Android模块不可用")
            # 回退到应用内部存储
            try:
                from android import mActivity
                context = mActivity.getApplicationContext()
                cache_dir = context.getExternalFilesDir(None)
                if cache_dir:
                    base_path = os.path.join(cache_dir.getAbsolutePath(), 'assets', 'animal_photos')
                    if not os.path.exists(base_path):
                        os.makedirs(base_path, exist_ok=True)
                else:
                    base_path = os.path.join('/data/data/org.kivy.enhancedquiz/files/assets/animal_photos')
                    if not os.path.exists(base_path):
                        os.makedirs(base_path, exist_ok=True)
            except Exception:
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
        try:
            os.makedirs(base_path, exist_ok=True)
            print(f"创建目录: {base_path}")
        except Exception as e:
            print(f"创建目录失败: {e}")
            return None
    
    return base_path

def get_file_md5(filepath):
    """获取文件MD5值"""
    if not os.path.exists(filepath):
        return None
    with open(filepath, 'rb') as f:
        return hashlib.md5(f.read()).hexdigest()

def sync_photos_from_oss(progress_callback=None):
    """从OSS同步照片"""
    if not OSS_AVAILABLE:
        print("OSS功能不可用，跳过同步")
        return 0, 0, 0
    
    print("开始同步OSS图片...")
    print(f"使用OSS配置: {ENDPOINT}, {BUCKET_NAME}")
    
    local_dir = get_local_photo_dir()
    print(f"本地目录: {local_dir}")
    print(f"目录是否存在: {os.path.exists(local_dir)}")
    
    if not os.path.exists(local_dir):
        print(f"错误: 本地目录不存在，无法同步")
        return 0, 0, 0
    
    try:
        auth = oss2.Auth(ACCESS_KEY_ID, ACCESS_KEY_SECRET)
        bucket = oss2.Bucket(auth, ENDPOINT, BUCKET_NAME)
    except Exception as e:
        print(f"OSS认证失败: {e}")
        return 0, 0, 0
    
    local_files = set()
    try:
        for f in os.listdir(local_dir):
            if f.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                local_files.add(f)
        print(f"本地文件数量: {len(local_files)}")
    except Exception as e:
        print(f"读取本地目录失败: {e}")
        return 0, 0, 0
    
    oss_files = {}
    try:
        print(f"开始列举OSS文件，前缀: {OSS_FOLDER}")
        for obj in oss2.ObjectIterator(bucket, prefix=OSS_FOLDER):
            if obj.key == OSS_FOLDER:
                continue
            filename = os.path.basename(obj.key)
            if filename.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.bmp')):
                oss_files[filename] = obj.key
        print(f"OSS文件数量: {len(oss_files)}")
    except Exception as e:
        print(f"列举OSS文件失败: {e}")
        return 0, 0, 0
    
    # 删除本地多余文件
    files_to_delete = local_files - set(oss_files.keys())
    print(f"需要删除的文件: {len(files_to_delete)}")
    for filename in files_to_delete:
        filepath = os.path.join(local_dir, filename)
        try:
            os.remove(filepath)
            print(f"已删除本地文件: {filename}")
        except Exception as e:
            print(f"删除文件失败 {filename}: {e}")
    
    # 同步OSS文件到本地
    total_files = len(oss_files)
    downloaded = 0
    skipped = 0
    
    for filename, oss_key in oss_files.items():
        local_path = os.path.join(local_dir, filename)
        
        need_download = False
        if not os.path.exists(local_path):
            need_download = True
            print(f"文件不存在，需要下载: {filename}")
        else:
            try:
                oss_meta = bucket.head_object(oss_key)
                local_size = os.path.getsize(local_path)
                oss_size = oss_meta.content_length
                if local_size != oss_size:
                    need_download = True
                    print(f"文件大小不同，需要下载: {filename} (本地:{local_size}, OSS:{oss_size})")
            except Exception as e:
                print(f"检查文件元数据失败 {filename}: {e}")
                need_download = True
        
        if need_download:
            try:
                print(f"开始下载: {filename}")
                bucket.get_object_to_file(oss_key, local_path)
                print(f"已下载: {filename}")
                downloaded += 1
            except Exception as e:
                print(f"下载文件失败 {filename}: {e}")
        else:
            skipped += 1
            print(f"跳过: {filename}")
        
        if progress_callback:
            progress_callback(downloaded + skipped, total_files, filename, need_download)
    
    print(f"\n同步完成!")
    print(f"下载: {downloaded} 个文件")
    print(f"跳过: {skipped} 个文件")
    print(f"删除: {len(files_to_delete)} 个文件")
    
    return downloaded, skipped, len(files_to_delete)

def get_photo_list():
    """获取本地照片列表"""
    local_dir = get_local_photo_dir()
    valid_ext = ('.jpg', '.jpeg', '.png', '.gif', '.bmp')
    
    if not os.path.exists(local_dir):
        return []
    
    files = [f for f in os.listdir(local_dir) if f.lower().endswith(valid_ext)]
    return [os.path.join(local_dir, f) for f in files]

if __name__ == "__main__":
    sync_photos_from_oss()

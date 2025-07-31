import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

EMBY_URL = os.getenv("EMBY_URL", "http://localhost:8096")
API_KEY = os.getenv("EMBY_API_KEY", "")
LIBRARY_IDS = os.getenv("EMBY_LIBRARY_ID", "")  # 逗号分隔的多个ID
WATCH_PATH = os.getenv("WATCH_PATH", "/watched")

library_id_list = [lib_id.strip() for lib_id in LIBRARY_IDS.split(",") if lib_id.strip()]

class WatchHandler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            print(f"[INFO] 检测到新文件: {event.src_path}")
            self.refresh_all_libraries()

    def refresh_all_libraries(self):
        for lib_id in library_id_list:
            url = f"{EMBY_URL}/emby/Library/Refresh"
            params = {
                "LibraryItemId": lib_id,
                "Recursive": "true",
                "ImageRefreshMode": "Default",
                "MetadataRefreshMode": "Default",
                "ReplaceAllMetadata": "false",
                "ReplaceAllImages": "false"
            }
            headers = {
                "X-Emby-Token": API_KEY
            }
            try:
                response = requests.post(url, params=params, headers=headers)
                print(f"[INFO] 刷新媒体库ID {lib_id}, 状态码: {response.status_code}")
            except Exception as e:
                print(f"[ERROR] 刷新媒体库ID {lib_id} 失败: {e}")

if __name__ == "__main__":
    if not os.path.exists(WATCH_PATH):
        print(f"[ERROR] 监听路径 {WATCH_PATH} 不存在，退出。")
        exit(1)

    event_handler = WatchHandler()
    observer = Observer()
    observer.schedule(event_handler, path=WATCH_PATH, recursive=True)
    observer.start()
    print(f"[INFO] 开始监听路径: {WATCH_PATH}")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

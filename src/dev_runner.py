import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

class RestartOnChange(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = None
        self.start_process()

    def start_process(self):
        if self.process:
            self.process.terminate()
        self.process = subprocess.Popen(self.command, shell=True)

    def on_modified(self, event):
        if event.src_path.endswith(".py"):
            print(f"\n🔁 Arquivo modificado: {event.src_path}")
            self.start_process()

if __name__ == "__main__":
    path = "."
    event_handler = RestartOnChange("python app.py")
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()

    print("👀 Aguardando modificações...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

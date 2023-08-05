# watch for changes and re-build

import os
import time
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from livereload import Server

DIST_PATH = "dist"
DIR_TO_WATCH = "pages"
COMMAND_TO_RUN = "python3 build.py"

def md_modified(event):
    # if event.is_directory(): return
    if event.src_path.endswith(".md"):
        print(f"detected change in file: {event.src_path}")
        subprocess.run(COMMAND_TO_RUN, shell=True)
        time.sleep(2)

def start_watching():
    event_handler = FileSystemEventHandler()
    event_handler.on_modified = md_modified

    observer = Observer()
    observer.schedule(event_handler, path=DIR_TO_WATCH, recursive=False)
    observer.start()

    print(f"watching for changes in {DIR_TO_WATCH}")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

def start_livereload():
    server = Server()
    server.watch(DIR_TO_WATCH)
    server.serve(root=DIST_PATH, open_url=False)

if __name__ == "__main__":
    livereload_thread = threading.Thread(target=start_livereload)
    livereload_thread.start()
    time.sleep(1)
    # watch for changes
    start_watching()
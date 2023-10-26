# watch for changes and re-build

import os
import sys
import time
import subprocess
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from livereload import Server

SOURCE_PATH = sys.argv[1] if len(sys.argv) > 1 else False
# TODO: get dist path from config file
# DIST_PATH = sys.argv[2] if len(sys.argv) > 2 else False
DIST_PATH = False
if SOURCE_PATH != False and os.path.exists(f"{SOURCE_PATH}/.md2website-config"):
    with open(f"{SOURCE_PATH}/.md2website-config", "r") as file:
        config_content = file.read()
        # parse config
        for line in config_content.split("\n"):
            CONFIG_NAME = str(line.split("=")[0].strip())
            if CONFIG_NAME == "DIST_PATH": DIST_PATH = str(line.split("DIST_PATH =")[1].strip()[1:-1])

if not SOURCE_PATH or not DIST_PATH:
    print("No source or dist folder provided, watching demo.")
    print("Usage: python3 watch.py <path/to/source> <path/to/dist>")
    SOURCE_PATH = "demo"
    DIST_PATH = "__dist"

DIR_TO_WATCH = "pages"
COMMAND_TO_RUN = f"python3 build.py {SOURCE_PATH}"

def md_modified(event):
    # if event.is_directory(): return
    if event.src_path.endswith(".md"):
        # print(f"detected change in file: {event.src_path}")
        subprocess.run(COMMAND_TO_RUN, shell=True)
        # TODO: fix this to reload once done building (how to only build file that changed?)
        time.sleep(1)

def start_watching():
    event_handler = FileSystemEventHandler()
    event_handler.on_modified = md_modified

    observer = Observer()
    observer.schedule(event_handler, path=DIR_TO_WATCH, recursive=False)
    observer.start()

    # print(f"watching for changes in {DIR_TO_WATCH}")

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
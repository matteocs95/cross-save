import time
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

class EventHandler(FileSystemEventHandler):

    def __init__(self, path, file_name, callback):
        self.path = path
        self.file_name = file_name
        self.callback = callback

        # set observer to watch for changes in the directory
        self.observer = Observer()
        self.observer.schedule(self, path, recursive=False)
        self.observer.start()
        self.observer.join()

    def on_modified(self, event):
        if not event.is_directory and event.src_path.endswith(self.file_name):
            self.observer.stop()
            self.callback()
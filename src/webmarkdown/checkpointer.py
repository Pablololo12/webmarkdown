from pathlib import Path
import os
import shutil

class Checkpointer:
    _instance = None
    created = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls.created = []
        return cls._instance

    def read(self):
        with open('.cache', 'r') as f:
            return [x.strip() for x in f.readlines()]

    def mrproper(self):
        lines = self.read()
        files = [l.split(',')[1] for l in lines if l.split(',')[0]=='f']
        directories = [l.split(',')[1] for l in lines if l.split(',')[0]=='d']
        for file in files:
            if os.path.exists(file):
                os.remove(file)
        for directory in directories:
            if os.path.exists(directory):
                shutil.rmtree(directory)
        self.remove()

    def remove(self):
        if os.path.exists(".cache"):
            os.remove(".cache")

    def file_created(self, file):
        if ('f', file) not in self.created:
            self.created.append(('f',file))

    def folder_created(self, folder):
        if ('d',folder) not in self.created:
            self.created.append(('d',folder))

    def write(self):
        path = Path(".cache")
        path.touch(exist_ok=True)
        with open('.cache', 'w') as f:
            for (t,file) in self.created:
                f.write(f"{t},{file}\n")

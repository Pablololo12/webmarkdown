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
        for file in self.read():
            if os.path.exists(file):
                os.remove(file)
        for file in self.read():
            p = Path(file)
            dirr = p.parent
            if dirr == Path("."):
                continue
            if dirr.exists():
                shutil.rmtree(dirr)
        self.remove()

    def remove(self):
        if os.path.exists(".cache"):
            os.remove(".cache")

    def file_created(self, file):
        self.created.append(file)

    def write(self):
        path = Path(".cache")
        path.touch(exist_ok=True)
        with open('.cache', 'a') as f:
            for file in self.created:
                f.write(f"{file}\n")

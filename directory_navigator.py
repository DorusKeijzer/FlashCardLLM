from contextlib import contextmanager
import os
import hashlib
import json


class directory_crawler:
    def __init__(self, root):
        self.hasher = hashlib.new("sha256")
        self.root = root

    def crawl(self):
        with change_dir(self.root):
            children = os.listdir()
            for child in children:
                yield child, self.hash(child)

    def hash(self, filepath):
        with open(filepath, "rb") as file:
            while chunk := file.read(8192):
                self.hasher.update(chunk)
        return self.hasher.hexdigest()

    def changed_files(self, json_path):
        hashes = json.load(json_path)
        for file, hash in self.crawl():
            if hashes[file] != hash:
                yield file
                hashes[file] = hash

    def create_json(self):
        json = os.path.join(os.)
        for text, hash in self.crawl():


@contextmanager
def change_dir(target_dir):
    """Changes back to the initial directory after the context manager is used"""
    old_dir = os.getcwd()  # Save the current working directory
    try:
        os.chdir(target_dir)
        yield
    finally:
        os.chdir(old_dir)  # Restore the original directory


if __name__ == "__main__":
    crawler = directory_crawler(os.path.join(os.getcwd(), "test"))

    for child, hash in crawler.crawl():
        print(child, hash)

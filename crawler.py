from contextlib import contextmanager
import os
import hashlib
import json


class directory_crawler:
    def __init__(self, root):
        self.root = root
        self.hash_path = os.path.join(self.root, "gen/hashes.json")
        os.makedirs(os.path.dirname(self.hash_path), exist_ok=True)

    def crawl(self, dir):
        """Returns all text files in a given directory as well as their hash"""
        with change_dir(dir):
            children = os.listdir()
            for child in children:
                if os.path.isdir(child):
                    childpath = os.path.join(os.getcwd(), child)
                    yield from self.crawl(childpath)

                elif os.path.splitext(child)[-1] == ".txt":
                    yield child, self.hash(child)

    def hash(self, filepath):
        hasher = hashlib.new("sha256")
        with open(filepath, "rb") as file:
            while chunk := file.read(8192):
                hasher.update(chunk)
        return hasher.hexdigest()

    def changed_files(self, update=False):
        """Only returns those files that have been changed since their last indexing"""
        with open(self.hash_path, "r") as json_file:
            hashes = json.load(json_file)
        for file, hash in self.crawl(self.root):
            if hashes[file] != hash:
                yield file, hash
                if update:
                    hashes[file] = hash
        if update:
            with open(self.hash_path, "w") as json_file:
                json.dump(hashes, json_file, indent=3)

    def create_json(self):
        hashes = {}

        for text, hash in self.crawl(self.root):
            hashes[text] = hash

        print(hashes)
        with open(self.hash_path, "w") as file:
            json.dump(hashes, file, indent=3)


@ contextmanager
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

    with open(crawler.hash_path, "r") as json_file:
        print(json.load(json_file))

    for child, hash in crawler.crawl(crawler.root):
        print(f"\033[1m{child}\033[0m, \n\thash: {hash}")

    for child, hash in crawler.changed_files(update=True):
        print(child, hash)

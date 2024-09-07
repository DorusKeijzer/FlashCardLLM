from crawler import directory_crawler
import anki_utils
import card_generator

from collections import deque
import json
import os


class dialogue_manager:
    def __init__(self):
        self.config_path = os.path.join(os.getcwd(), "config.json")
        print(self.config_path)

    def couple_deck_to_dir(self):
        print("Which directory should we couple with which deck?")
        dir_name = input("Please specify the path to the directory: ")
        new_or_existing = input("New or existing deck? [(n)ew, (e)xisting]: ")

        if new_or_existing.lower().strip() in ["e", "existing"]:
            self.print_directories()

        deck_name = input("Please specify the name of the deck: ")

        # Ensure config file exists and is loaded
        if not os.path.exists(self.config_path):
            with open(self.config_path, "w") as config_file:
                json.dump({}, config_file)

        with open(self.config_path, "r+") as config_file:
            try:
                config = json.load(config_file)
            except json.JSONDecodeError:
                config = {}

            config[dir_name] = deck_name
            # Move the file pointer to the start before writing
            config_file.seek(0)
            json.dump(config, config_file, indent=3)
            # Truncate the file to the current size to avoid leftover data
            config_file.truncate()

    def print_directories(self):
        with open(self.config_path, "r") as config_file:
            config = json.load(config_file)
        for i, key in enumerate(config.keys(), start=1):
            print(f"{i}. {key}")
        if len(config.keys()) == 0:
            print("No coupled directories found")


def fill_deck(dir):
    dc = directory_crawler()
    for file in dc.crawl(dir):
        card = generate_card(file)


def main():
    dm = dialogue_manager()
    dm.print_directories()
    dm.couple_deck_to_dir()


if __name__ == "__main__":
    main()

import os

PATH = os.path.join("data", "australia_nsw_sample")


def search(path: str):
    dir_name = os.listdir(PATH)[0]
    final_path = os.path.join(PATH, dir_name)
    files = os.listdir(final_path)
    for file_name in files:
        with open(os.path.join(final_path, file_name), "r") as file:
            data = "".join(file.readlines())
            if "princes highway upgrade program - aboriginal" in data.lower():
                print(f"FOUND FOR {file_name}")


def run(*args):
    search(PATH)

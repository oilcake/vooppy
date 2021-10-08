import os

SUPPORTED = ['.mp4', '.mpg', '.mov', '.avi', '.wmv', '.mkv']


def filter_files(path_to_files, prefix):
    path = os.path.abspath(path_to_files)
    for root, dirs, files in os.walk(path):
        for file in files:
            if supported(file):
                if file.startswith(prefix):
                    print(file)
                    yield(os.path.join(root, file))


def supported(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension in SUPPORTED

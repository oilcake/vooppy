import os
import itertools
import random

from thefuzz import process


EXCLUSIONS = [".DS_Store", ".com.greenworldsoft.syncfolderspro"]
SUPPORTED = [".mp4", ".mpg", ".mov", ".avi", ".wmv", ".mkv"]


def get_len(iter):
    return len(list(iter))


def unpack_tuple(sometuple):
    (name, relevance) = sometuple
    return str(name)


def unpack_processed(list):
    for unit in list:
        unpacked = unpack_tuple(unit)
        yield unpacked


def filter_with_prefix(path_to_files, prefix, file, with_fuzz):
    path = os.path.abspath(path_to_files)
    if not with_fuzz:
        found_by_name = filter_files(path, prefix)
        return found_by_name
    coll = []
    found = filter_files(path, prefix)
    file_mask = os.path.basename(file)
    print(file_mask)
    get_it = process.extract(file, found, limit=30)
    for name_ in get_it:
        name = unpack_tuple(name_)
        coll.append(name)
    if len(list(coll)) == 0:
        found_by_name = filter_files(path, prefix)
    found_by_name = coll
    for item in found_by_name:
        print(item)
    return found_by_name


def filter_files(path, prefix):
    for root, dirs, files in os.walk(path):
        for file in files:
            if supported(file):
                if file.startswith(prefix):
                    yield (os.path.join(root, file))


def get_folders(path_to_dirs):
    folders = os.listdir(path_to_dirs)
    path = os.path.abspath(path_to_dirs)
    cat = map(os.path.join, itertools.repeat(path), folders)

    return cat


def supported(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension in SUPPORTED


def folder(pre_folder):
    fld = os.listdir(pre_folder)
    return fld


def best_match(file, folder):
    files = filter_files(folder, "")
    match = process.extract(file, files, limit=10)
    no_duplicates = filter(lambda x: x != (file, 100), match)
    files = list(map(unpack_tuple, no_duplicates))
    name = random.choice(files)
    print("first in is", name)
    return name


def stripped_name(file):
    return {"name": os.path.basename(file), "path": file}

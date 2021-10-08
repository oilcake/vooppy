import os

from fuzzywuzzy import process

EXCLUSIONS = ['.DS_Store', '.com.greenworldsoft.syncfolderspro']
SUPPORTED = ['.mp4', '.mpg', '.mov', '.avi', '.wmv', '.mkv']


def unpack_tuple(pair):
    # print('in', type(pair))
    (name, relevance) = (pair)
    # print('unp', name)
    return str(name)


def unpack_processed(list):
    for unit in list:
        # print(unit)
        unpacked = unpack_tuple(unit)
        # print(unpacked)
        yield unpacked


def filter_with_prefix(path_to_files, prefix, file, with_fuzz):
    path = os.path.abspath(path_to_files)
    if not with_fuzz:
        found_by_name = filter_files(path, prefix)
        return found_by_name
    coll = []
    found = filter_files(path, prefix)
    get_it = process.extract(file, found, limit=3)
    # print(get_it)
    for name_ in get_it:
        # print(type(name_), name_)
        name = unpack_tuple(name_)
        # print(type(name), name)
        coll.append(name)
    # coll = list(map(unpack_processed, get_it))
    # print(coll)
    # print('fuzz list', list(coll))
    if len(list(coll)) == 0:
        found_by_name = filter_files(path, prefix)
    found_by_name = coll
    print(found_by_name)
    return found_by_name


def filter_files(path, prefix):
    for root, dirs, files in os.walk(path):
        for file in files:
            if supported(file):
                if file.startswith(prefix):
                    yield(os.path.join(root, file))


def supported(file):
    filename, file_extension = os.path.splitext(file)
    return file_extension in SUPPORTED

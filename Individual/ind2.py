#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from pathlib import Path
from itertools import islice

space = '    '
branch = '│   '
tee = '├── '
last = '└── '


def tree(dir_path, level=-1, limit_to_directories=False,
         length_limit=1000):
    dir_path = Path(dir_path)
    files = 0
    directories = 0

    def inner(dir_path, prefix='', level=-1):
        nonlocal files, directories
        if not level:
            return
        if limit_to_directories:
            contents = [d for d in dir_path.iterdir() if d.is_dir()]
        else:
            contents = list(dir_path.iterdir())
        pointers = [tee] * (len(contents) - 1) + [last]
        for pointer, path in zip(pointers, contents):
            if path.is_dir():
                yield prefix + pointer + path.name
                directories += 1
                extension = branch if pointer == tee else space
                yield from inner(path, prefix=prefix + extension,
                                 level=level - 1)
            elif not limit_to_directories:
                yield prefix + pointer + path.name
                files += 1

    print(dir_path.name)
    iterator = inner(dir_path, level=level)
    for line in islice(iterator, length_limit):
        print(line)
    if next(iterator, None):
        print(f'... length_limit, {length_limit}, reached, counted:')
    print(
        f'\n{directories} directories' + (f', {files} files' if files else ''))


if __name__ == "__main__":
    print("This program is showing files and directories on C: drive or CWD")
    option = input("Where do you want to work? h - home, c - CWD: ")
    if option == "h":
        directory = input("Type the directory name: ")
        lvl = int(input("Enter the level of search if needed (-1) if don't: "))
        limit_d = input("Do you want to print only the directories? d - yes: ")
        if limit_d == "d":
            if lvl > 0:
                tree(Path.home() / directory, lvl, True)
            else:
                tree(Path.home() / directory, True)
        else:
            if lvl > 0:
                tree(Path.home() / directory, lvl)
            else:
                tree(Path.home() / directory)
    if option == "c":
        lvl = int(input("Enter the level of search if needed (-1) if don't: "))
        limit_d = input("Do you want to print only the directories? d - yes: ")
        if limit_d == "d":
            if lvl > 0:
                tree(Path.cwd(), lvl, True)
            else:
                tree(Path.cwd(), True)
        else:
            if lvl > 0:
                tree(Path.cwd(), lvl)
            else:
                tree(Path.cwd())

#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

LIST_FILE = 'list.txt'

def main():
    files = os.listdir('csv')
    files.sort()
    files.reverse()

    with open(LIST_FILE, mode='w') as f:
        for file in files:
            f.write(file + '\n')

if __name__ == '__main__':
    main()

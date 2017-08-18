from sys import argv, exit
import re

def usage():
    print("{0} path", argv[0])
    exit(1)

def process(data):
    pass # no more for today... STUDY YOU PIECE OF SH!T

def main():
    if len(argv) != 2:
        usage()
    
    path = argv[1]

    with open(path) as f:
        process(f)

if __name__ == '__main__':
    main()
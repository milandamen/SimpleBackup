import sys

def uPrint(string):
    print(string.encode(sys.stdout.encoding, errors='replace').decode(sys.stdout.encoding))
class CorruptDiffListException(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)
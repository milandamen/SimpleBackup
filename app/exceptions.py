class InvalidOperationForNonBuildModeException(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)

class InvalidSnapshotModeException(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)
        
class CorruptDiffListException(Exception):
    def __init__(self, mismatch):
        Exception.__init__(self, mismatch)
import os
import time
import codecs
import app.exceptions

##
# Make a snapshot of all files in the sourcePath directory tree
##

class Snapshot:
    def __init__(self):
        self.fileList = []                              # List to be populated elsewhere
        self.saveDate = None
        self.sourcePath = ''
        self.count = 0
    
    def write(self, string):
        self.fileList.append(string)
        self.count += 1
    
    def toList(self):
        return self.fileList
    
    def __repr__(self):
        s = ''
        for line in self.fileList:
            s += line + '\n'
        return s
    
    def __len__(self):
        return self.count
            

# Get and save file list (snapshot)
def generateSnapshot(sourcePath):
    print('Generating snapshot..')
    
    files = generateFileList(sourcePath)
    
    if len(files):
        snapshot = Snapshot()
        snapshot.sourcePath = sourcePath
        snapshot.write(sourcePath)                      # Put sourcePath on first line
        
        for file in files:
            try:
                mtime = int(os.path.getmtime(file))        # File last modified time, can give an exception if file path is too long in Windows
                snapshot.write('' + str(mtime) + '\t' + file)
            except OSError:
                pass

        print('Generated snapshot.')
        print('Saving snapshot to disk..')
        
        writeSnapshot(snapshot)
        
        print('Snapshot saved to disk.\n')
        
        return snapshot
    else:
        print('No files found in directory: %s' % sourcePath)

# Get all files in the directory tree from sourcePath
def generateFileList(sourcePath):
    fileList = []
    count = 0
    for (path, dirs, files) in os.walk(sourcePath):
        for filename in files:
            fileList.append(os.path.join(path, filename))
            count += 1
            if count % 5000 == 0:
                print('Scanned %i files so far..' % count)
            
    return fileList
    
# Write snapshot to disk
def writeSnapshot(snapshot):
    saveDate = int(time.time())
    
    f = codecs.open('snapshots/%s.snapshot' % saveDate, encoding='utf-16', mode='w')        # Make a file with current time in seconds as name
    f.write(str(snapshot))
    f.close()
    
    snapshot.saveDate = saveDate

# Get previous snapshot from disk using input snapshot as reference or use latest snapshot
def getPrevious(snapshot):
    if snapshot and snapshot.saveDate == None:
        return
    
    snapshots = []
    for (path, dirs, files) in os.walk('snapshots'):
        snapshots.extend(files)
        break
    
    snapshots = [ fi for fi in snapshots if fi.endswith(".snapshot") ]
        
    lastPath = None
    lastSaveDate = 0
    while len(snapshots):
        for file in snapshots:
            try:
                curSaveDate = int(file[:-len('.snapshot')])
                if curSaveDate > lastSaveDate and (snapshot == None or curSaveDate < snapshot.saveDate):
                    lastPath = file
                    lastSaveDate = curSaveDate
            except ValueError:
                pass
        
        if lastPath == None:
            return
        
        if snapshot == None or validSnapshotSourcePath(lastPath, snapshot.sourcePath):
            return readSnapshot(lastPath)
        else:
            snapshots.remove(lastPath)
            lastPath = None

# Determine if the found snapshot has the same source path as the current snapshot
def validSnapshotSourcePath(snapshotPath, sourcePath):
    f = codecs.open('snapshots/' + snapshotPath, encoding='utf-16', mode='r')
    valid = f.readline().strip('\n') == sourcePath
    f.close()
    return valid
    
# Get the last snapshot
def getLast():
    return getPrevious(None)

# Load a snapshot from file
def readSnapshot(snapshotPath):
    snapshot = Snapshot()
    snapshot.saveDate = int(snapshotPath[:-len('.snapshot')])
    firstLine = True
    
    f = codecs.open('snapshots/' + snapshotPath, encoding='utf-16', mode='r')
    
    for line in f:
        if firstLine:
            if line != '' and line != '\n':
                snapshot.sourcePath = line.strip('\n')
                snapshot.write(line.strip('\n'))
                
            firstLine = False
            continue
        
        if line != '' and line != '\n':
            snapshot.write(line.strip('\n'))
    
    f.close()
    
    print('Loaded snapshot %s.' % snapshotPath)
    
    return snapshot
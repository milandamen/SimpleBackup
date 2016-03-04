import os
import sys
import io
import time
import codecs
import app.snapshot as app_snapshot
import app.exceptions
import app.helpers as helpers

##
# Compare 2 snapshots to eachother
##

class DiffCounterHelper:
    def __init__(self, maxLen):
        self.count = 0
        self.maxLen = maxLen * 2
        self.lastPercentage = 0
        
    def increment(self):
        self.count += 1
        percentage = int((self.count / self.maxLen) * 100)
        if percentage - self.lastPercentage >= 5:
            print('Compared ' + str(percentage) + '% of files so far..')
            self.lastPercentage = percentage
        return True

# Return a list of files that changed between this snapshot and the previous one
def generateDiffList(snapshot):
    prevSnapshot = app_snapshot.getPrevious(snapshot)
    
    if not prevSnapshot:
        print('No earlier snapshot found for the given date and source path.')
        printDiffList(snapshot)
        print('')
        print('No further action required.')
        return snapshot.toList()
        
    print('Generating diff list..')
    diffList = diffSnapshots(prevSnapshot, snapshot)
    print('Generated diff list.\n')
    
    printDiffList(diffList)
    
    print('\nSaving difference to disk..')
    diffFileName = writeDiffList(diffList)
    print('Difference saved to disk as %s.' % diffFileName)
    print('')
    print('Open the diff file in a text editor and remove lines of files you don\'t want to copy. DO NOT REMOVE THE FIRST LINE.')
    print('Then open SimpleBackup again and select option 3 to start the backup process.')
    
    return diffList

# Compare 2 snapshots; outputs new and changed files
def diffSnapshots(prevSnapshot, snapshot):
    l_prevSnapshot = prevSnapshot.toList()
    l_snapshot = snapshot.toList()
    
    diffCounterHelper = DiffCounterHelper(len(l_snapshot))
    diffList = [x for x in l_snapshot if x not in l_prevSnapshot and diffCounterHelper.increment()]       # Get new or changed files compared to prevSnapshot
    
    finalDiffList = [snapshot.sourcePath]
    for line in diffList:
        if line != '' and line != '\n':
            try:
                finalDiffList.append(line[line.index('\t') + 1:])
            except ValueError:
                pass
    
    return finalDiffList

# Write differences to disk
def writeDiffList(diffList):
    saveDate = int(time.time())
    
    f = codecs.open('snapshots/%s.diff' % saveDate, encoding='utf-16', mode='w')            # Make a file with current time in seconds as name
    for path in diffList:
        f.write(path + '\n')
    f.close()
    
    return '%s.diff' % saveDate                         # Return new filename
    
# Get last difflist from disk
def getLast():
    diffs = []
    for (path, dirs, files) in os.walk('snapshots'):
        diffs.extend(files)
        break
    
    diffs = [ fi for fi in diffs if fi.endswith(".diff") ]
        
    lastPath = None
    lastSaveDate = 0
    while len(diffs):
        for file in diffs:
            try:
                curSaveDate = int(file[:-len('.diff')])
                if curSaveDate > lastSaveDate:
                    lastPath = file
                    lastSaveDate = curSaveDate
            except ValueError:
                pass
        
        if lastPath == None:
            return
        
        return readDiffList(lastPath)

# Load a difflist from file
def readDiffList(diffPath):
    diffList = []
    
    f = codecs.open('snapshots/' + diffPath, encoding='utf-16', mode='r')
    
    for line in f:
        if line != '' and line != '\n':
            diffList.append(line.strip('\n'))
    
    f.close()
    
    if len(diffList) == 0:
        raise app.exceptionsCorruptDiffListException('Diff file does not have any lines!')
    if not os.path.isdir(diffList[0]):
        raise app.exceptionsCorruptDiffListException('First line of diff file is not source path!')
    
    print('Loaded diff %s\n' % diffPath)
    
    return diffList


# Print the new and changed files when 2 snapshots are compared
def printDiffList(list):
    print('New or changed files:')
    print('----------------------')
    
    if len(list) > 30:
        print('(List too long to display)')
        return
    
    if isinstance(list, app_snapshot.Snapshot):
        for line in list.toList():
            helpers.uPrint(line)
    else:
        firstLine = True
        for line in list:
            if firstLine:
                firstLine = False
                continue
                
            helpers.uPrint(line)
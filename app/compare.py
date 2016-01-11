import snapshot as app_snapshot
import os
import time
import exceptions

##
# Compare 2 snapshots to eachother
##

# Return a list of files that changed between this snapshot and the previous one
def generateDiffList(snapshot):
    prevSnapshot = app_snapshot.getPrevious(snapshot)
    
    if not prevSnapshot:
        print 'No earlier snapshot found for the given date and source path'
        printDiffList(snapshot)
        return snapshot.toList()
    
    diffList = diffSnapshots(prevSnapshot, snapshot)
    
    printDiffList(diffList)
    
    print '\nSaving difference to disk..'
    diffFileName = writeDiffList(diffList)
    print 'Difference saved to disk as ' + diffFileName
    
    return diffList

# Compare 2 snapshots; outputs new and changed files
def diffSnapshots(prevSnapshot, snapshot):
    l_prevSnapshot = prevSnapshot.toList()
    l_snapshot = snapshot.toList()
    
    diffList = [x for x in l_snapshot if x not in l_prevSnapshot]       # Get new or changed files compared to prevSnapshot
    if snapshot.mode == 'build' and prevSnapshot.mode == 'read':
        diffList.pop(0)
    
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
    saveDate = long(time.time())
    
    f = open('snapshots/%s.diff' % saveDate, 'w')   # Make a file with current time in seconds as name
    for path in diffList:
        f.write(path + '\n')
    f.close()
    
    return '%s.diff' % saveDate                     # Return new filename
    
# Get last difflist from disk
def getLast():
    diffs = []
    for (path, dirs, files) in os.walk('snapshots'):
        diffs.extend(files)
        break
    
    diffs = [ fi for fi in diffs if fi.endswith(".diff") ]
        
    lastPath = None
    lastSaveDate = 0L
    while len(diffs):
        for file in diffs:
            try:
                curSaveDate = long(file[:-len('.diff')])
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
    
    f = open('snapshots/' + diffPath, 'r')
    
    for line in f:
        if line != '' and line != '\n':
            diffList.append(line.strip('\n'))
    
    f.close()
    
    if len(diffList) == 0:
        raise CorruptDiffListException('Diff file does not have any lines')
    if not os.path.isdir(diffList[0]):
        raise CorruptDiffListException('First line of diff file is not source path')
    
    print 'Loaded diff %s\n' % diffPath
    #printDiffList(diffList)
    
    return diffList


# Print the new and changed files when 2 snapshots are compared
def printDiffList(list):
    print 'New or changed files:'
    print '----------------------'
    
    if len(list) > 30:
        print '(List too long to display)'
        return
    
    if isinstance(list, app_snapshot.Snapshot):
        print list
    else:
        firstLine = True
        for line in list:
            if firstLine:
                firstLine = False
                continue
                
            print line
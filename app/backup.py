import shutil
import os

def copyFiles(diffList):
    sourcePath = diffList[0]
    
    if not os.path.isdir(sourcePath):
        print 'Source path is not a directory: ' + sourcePath
        return
        
    destPath = raw_input('Enter the destination path to copy files to: ')
    if not os.path.isdir(destPath):
        print 'Destination path is not a directory: ' + sourcePath
        return
    
    if sourcePath[-1:] != '/':
        sourcePath += '/'
    if destPath[-1:] != '/':
        destPath += '/'
        
    sourcePathLength = len(sourcePath)
    
    print '\nStarting copying of files..'
    
    errorCount = 0L
    ignoreErrors = False
    firstLine = True
    for file in diffList:
        if firstLine:
            firstLine = False
            continue
        
        if os.path.isfile(file):
            try:
                destFilePath = destPath + file[sourcePathLength:]
                destFileDir = os.path.dirname(destFilePath)
                
                if not os.path.isdir(destFileDir):              # Check if directory exists to copy file directly into
                    os.makedirs(destFileDir)                    # Recursively make the directories
                
                shutil.copyfile(file, destFilePath)
            except Exception, e:
                print 'Error copying file %s: %s' % (file, str(e))
                errorCount += 1
        else:
            print 'Error copying file %s: path is not a file' % file
            errorCount += 1
            
        if ignoreErrors == False and errorCount >= 20:
            response = raw_input('Encountered 20 errors. Do you want to continue? (y/N): ').lower()
            if response == 'y':
                ignoreErrors = Trie
            else:
                break
    
    print '\nFinished.'
    print 'Encountered a total of %i errors' % errorCount
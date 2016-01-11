import os
import time
import app
import os

print 'SimpleBackup by D\'Arvit!'
print 'Site: darvit.nl\n'

print 'Available options:'
print '1: Generate new snapshot'
print '2: Use last snapshot'
print '3: Use last diff file'
print 'q: Exit SimpleBackup'

response = raw_input('Run option: ').lower()
print ''

if response == 'q':
    exit()

option = None
snapshot = None
diffList = None
if response == '1':
    option = 'snapshot'
    
    while True:
        sourcePath = raw_input('Enter the path from which you want to snapshot: ')
        if os.path.isdir(sourcePath):
            break
    
    snapshot = app.snapshot.generateSnapshot(sourcePath)
if response == '2':
    option = 'snapshot'
    snapshot = app.snapshot.getLast()
if response == '3':
    option = 'difflist'
    diffList = app.compare.getLast()

if option == 'snapshot':
    if snapshot == None:
        exit()
    
    print 'Source path: ' + snapshot.sourcePath
    print ''
    app.compare.generateDiffList(snapshot)
    print ''
    print 'Open the diff file in a text editor and remove lines of files you don\'t want to copy. DO NOT REMOVE THE FIRST LINE.'
    print 'Then open SimpleBackup again and select option 3 to start the backup process.'

if diffList and len(diffList) > 0:
    app.backup.copyFiles(diffList)

    
print '\nSimpleBackup has stopped.'


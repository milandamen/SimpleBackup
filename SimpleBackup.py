#!python3

import os
import time
import app
import os
import sys

print('SimpleBackup by D\'Arvit!')
print('Site: darvit.nl\n')

print('Available options:')
print('1: Generate new snapshot')
print('2: Use last snapshot')
print('3: Use last diff file')
print('q: Exit SimpleBackup')

response = input('Run option: ').lower()
print('')

if response == 'q':
    exit()
if response != '1' and response != '2' and response != '3':
    print('Entered invalid mode option: ' + response)
    exit(-1)

option = None
snapshot = None
diffList = None
if response == '1':
    option = 'snapshot'
    
    while True:
        sourcePath = '' + input('Enter the path from which you want to snapshot: ')
        if os.path.isdir(sourcePath):
            break
        else:
            print('No directory with this name exists: ' + sourcePath)
    
    snapshot = app.snapshot.generateSnapshot(sourcePath)
if response == '2':
    option = 'snapshot'
    snapshot = app.snapshot.getLast()
if response == '3':
    option = 'difflist'
    diffList = app.compare.getLast()

if option == 'snapshot':
    if snapshot == None:
        print('Snapshot could not be loaded.')
        exit(-1)
    
    print('Source path: ' + snapshot.sourcePath)
    print('')
    app.compare.generateDiffList(snapshot)              # Note this function does not update variable diffList, this is intended.

if diffList and len(diffList) > 0:
    app.backup.copyFiles(diffList)

    
print('\nSimpleBackup has stopped.')


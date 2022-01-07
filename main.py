import os
import sys
import re

from ast import literal_eval
MUSICTYPES = ['mp3', 'm4b']
DEBUG = False






def tagfile(file, track, title,  artist, album, year):
    #print(track, ') ', title, artist, album, year)
    command = 'id3tag'
    if track != '':
        command += " -t '" + track + "'"
    if title != '':
        command += " -s \"" + title  + "\""
    if artist != '':
        command += " -a \"" + artist + "\""
    if album != '':
        command += " -A \"" + album + "\""
    if year != '':
        command += " -y '" + year + "'"
    command += " \""+file+"\""




    if not DEBUG:
        os.system(command) 
    else: print(command)

    return

def get_information(file):
    if file.rsplit('.',1)[-1] not in MUSICTYPES:
            return

    vett = file.split('/')
    dirs = vett[:-1]
    title = vett[-1].rsplit('.',1)[0]

    track = ''
    album = ''
    artist = ''
    year = ''
   
    if re.fullmatch('[0-9]+ *- *.*', title):
        track = title.split('-', 2)[0].strip()
        title = title.split('-', 2)[1].strip()
    
    if len(dirs) >= 1:
        album = dirs[-1]
        if re.fullmatch('.*\([0-9]{4}\)', album):
            year = album.split('(')[-1][:-1].strip()
            album = album.rsplit('(', 1)[0].strip()
    if len(dirs) >= 2:
        artist = dirs[-2].strip()
 
    tagfile(file, track, title, artist, album, year)

def recursive_scan(path):
    if os.path.isfile(path):
        get_information(path)
        return
    dir = os.listdir(path)
    for file in dir:
        if file not in ign_folders:
            recursive_scan(path + '/' + file)


rootdir = '.'
args = {}

if len(sys.argv) >= 2:
    rootdir = sys.argv[-1]
    if rootdir[-1] == '/':
        rootdir = rootdir[:-1]
    for arg in sys.argv:
        if arg[:2] == '--':
            vett = arg[2:].split('=', 1)
            key = vett[0]
            value = vett[1] if len(vett) > 1 else True
            args[key] = value

ign_folders = []

DEBUG = args['debug'] if 'debug' in args.keys() else False

if 'ignore-folder' in args.keys():
    ign_folders = literal_eval( args['ignore-folder'])
    print('ignoring', ign_folders)
recursive_scan(rootdir)


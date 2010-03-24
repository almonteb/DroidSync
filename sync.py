###############################################################################
# 
# Author    : Brendan Almonte (almonteb@datawh.net)
# Company   : Data Warehouse
# Date      : 03-23-2010
# Filename  : sync.py
#
###############################################################################
#
#      Tested Version Info
# O/S       : Tested on Snow Leopard 10.6.2
# Python    : Python 2.6.1
# iTunes.py : iTunes version 0.2 (18) by Dave Bayer
#             (http://www.math.columbia.edu/~bayer/Python/iTunes/)
#
###############################################################################
#
#      Usage
# python sync.py [playlist_name] [copy directory]
#
###############################################################################
#
#      Description
# Start by getting list of files in playlist
# Compare files in playlist to whats already in the directory
# if in directory.. ignore
# if in directory and not on playlist... remove
# if not in directory and on playlist... add
#
###############################################################################

import os, sys, codecs, glob
import xml.etree.ElementTree as ET
import shutil

from appscript import *
from iTunes import *

###############################################################################
# Misc Functions
###############################################################################
def print_header(title):
    print "\n*******************************************************************************\n"
    print title
    print "\n*******************************************************************************\n"

def clean(str):
    # Expandability for more chars to be replaced in the future
    ret = str.replace('/', '-')
    return ret
        
def get_files(dir):
    files = glob.glob(os.path.join(dir, '*.*'))
    ret = []
    for file in files:
        ret.append(file.split('/').pop())
    return ret

def clean_dir(tracks, directory):
    print_header("Performing cleanup")
    # Clean files
    for file in glob.glob(directory + "/*/*/*.*"):
        arr    = file.split("/")
        name   = clean(arr.pop())
        album  = clean(arr.pop())
        artist = clean(arr.pop())
        print "Artist: " + artist
        print "Album : " + album
        print "Track : " + name
        
        found = False
        
        # TODO: Figure out more efficient way of doing this...
        for t in tracks:
            
            # Gather track info
            track_name = clean(t.location().path.split('/').pop())
            if t.artist() == "":
                track_artist = "Unknown Artist"
            else:
                track_artist = clean(t.artist())
            if t.album() == "":
                track_album = "Untitled"
            else:
                track_album = clean(t.album())
                
            if track_artist == artist:
                if track_album == album:
                    if track_name == name:
                        found = True
        
        if not found:
            print "Track will be removed..."
            os.remove(directory + "/" + artist + "/" + album + "/" + name)
        else:
            print "Track will not be removed..."
    
    # Clean empty directories
    for artist in glob.glob(directory + "/*"):
        if os.path.exists(artist + "/.DS_Store"):
            os.remove(artist + "/.DS_Store")
        for album in glob.glob(artist + "/*"):
            if os.path.exists(album + "/.DS_Store"):
                os.remove(album + "/.DS_Store")
            if not os.listdir(album):
                os.rmdir(album)
        if not os.listdir(artist):
            os.rmdir(artist)

def sync_playlist(playlist, directory):
    pl      = get_playlists()
    files   = get_files(directory)
    
    for p in pl:
        if p.name() == playlist:
            tracks = get_tracks(p)

            # Copy...
            print_header("Copying tracks")
            for t in tracks:
                
                # Gather track info
                cur_track = clean(t.location().path.split('/').pop())
                if t.artist() == "":
                    artist = "Unknown Artist"
                else:
                    artist = clean(t.artist())
                print "Artist: " + artist
                if t.album() == "":
                    album = "Untitled"
                else:
                    album = clean(t.album())
                print "Album : " + album
                print "Track : " + t.name()
                if os.path.exists(directory + "/" + artist + "/" + album + "/" + cur_track):
                    print t.name() + " is already copied...\n"
                else:
                    print t.name() + " will be copied...\n"
                    
                    # Check directory structure exists
                    if not os.path.exists(directory + "/" + artist):
                        os.mkdir(directory + "/" + artist)
                    if not os.path.exists(directory + "/" + artist + "/" + album):
                        os.mkdir(directory + "/" + artist + "/" + album)
                    shutil.copy2(t.location().path, directory + "/" + artist + "/" + album)
            
            # Clean up
            clean_dir(tracks, outdir)

###############################################################################
# Main
###############################################################################
if len(sys.argv) is not 3:
    print "usage: [playlist_name] [copy directory]"
    sys.exit()

outdir  = sys.argv[2]
pl_name = sys.argv[1]

if not os.path.exists(outdir):
    print "directory: " + outdir + " doesn't exist...\n"
    sys.exit()

print_header("Playlist: " + pl_name)
sync_playlist(pl_name, outdir)
print_header("Sync of playlist " + pl_name + " complete!")


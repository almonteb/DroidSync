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
# Usage: python sync.py [playlist_name] [copy directory]
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

import os, sys,codecs, glob
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

def get_files(dir):
    files = glob.glob(os.path.join(dir, '*.mp3'))
    ret = []
    for file in files:
        ret.append(file.split('/').pop())
    return ret

def get_track_names(tracks):
    ret = []
    for track in tracks:
        ret.append(track.location().path.split('/').pop())
    return ret
    
def sync_playlist(playlist, directory):
    pl      = get_playlists()
    files   = get_files(directory)
    
    for p in pl:
        if p.name() == pl_name:
            tracks = get_tracks(p)

            # Copy...
            print_header("Copying tracks")
            for t in tracks:
                cur_track = t.location().path.split('/').pop()
                if cur_track in files:
                    print t.name() + " is already copied...\n"
                else:
                    print t.name() + " will be copied...\n"
                    shutil.copy(t.location().path, outdir)
            
            # Clean...
            print_header("Performing cleanup")
            track_names = get_track_names(tracks)
            for file in files:
                if file not in track_names:
                    print file + " will be removed...\n"
                    os.remove(directory + "/" + file)
                else:
                    print file + " will not be removed...\n"

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


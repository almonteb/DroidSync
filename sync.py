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
# O/S       : Tested on Snow Leopard 10.6.2 and Yosemity 10.10.3
# Python    : Python 2.6.1 and 2.7.8
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

from __future__ import print_function
import os
import sys
import shutil
from appscript import app

###############################################################################
# Misc Functions
###############################################################################


def print_header(title):
    """
    Generate a shiny header banner using the title string and lots of stars.

    :rtype : str
    """
    print(u"\n{0}\n{1}\n{0}".format('*' * 80, title))


def get_relative_filenames(directory):
    if not directory.endswith('/'):
        directory += '/'
    ret = []
    for root, dirs, files in os.walk(directory):
        relative_path = root[len(directory):]
        for f in files:
            ret.append(os.path.join(relative_path, f))
    return ret


def clean_droid_dir(directory):
    """
    Clean empty directories

    :param directory: The folder to scan for empty folders
    :return:
    """
    print_header("Performing cleanup")
    for root, dirs, files in os.walk(directory):
        if '.DS_Store' in files:
            os.remove(os.path.join(root, '.DS_Store'))

    for root, dirs, files in os.walk(directory, True):
        if len(dirs) == 0 and len(files) == 0:
            print('Remove dir {}'.format(root))
            os.removedirs(root)

def sync_playlist(playlist_name, target_directory):
    # iTunes integration taken from
    # http://www.math.columbia.edu/%7Ebayer/Python/iTunes/
    files_in_playlists = []
    print_header("Collecting tracks")
    for playlist in app('iTunes').user_playlists():
        if playlist.name() == playlist_name:
            for t in playlist.file_tracks():
                files_in_playlists.append(t.location().path)

    itunes_music_folder = os.path.commonprefix(files_in_playlists)
    files_in_playlists = \
        [f.replace(itunes_music_folder, '') for f in files_in_playlists]
    files_on_droid = get_relative_filenames(target_directory)

    to_be_copied = [x for x in files_in_playlists if x not in files_on_droid]
    to_be_ignored = [x for x in files_in_playlists if x in files_on_droid]
    to_be_removed = [x for x in files_on_droid if x not in files_in_playlists]

    print_header("Ignoring tracks found on droid and in playlist")
    if len(to_be_ignored):
        for f in to_be_ignored:
            print(u"Ignore {}".format(f))
    else:
        print(u"Nothing to ignore.")

    print_header("Copying tracks found in playlist, but not on droid")
    if len(to_be_copied):
        for f in to_be_copied:
            print(u"Copy {}".format(f))
            target_dirname = os.path.join(target_directory, os.path.dirname(f))
            if not os.path.exists(target_dirname):
                os.makedirs(target_dirname)
            shutil.copy2(os.path.join(itunes_music_folder, f), target_dirname)
    else:
        print(u"Nothing to copy.")

    print_header("Removing tracks found on droid, but not in playlist")
    if len(to_be_removed):
        for f in to_be_removed:
            print(u"Renove {}".format(f))
            os.remove(os.path.join(target_directory, f))
    else:
        print(u"Nothing to remove.")

    clean_droid_dir(target_directory)

###############################################################################
# Main
###############################################################################
if len(sys.argv) is not 3:
    print(u"usage: [playlist_name] [copy directory]")
    sys.exit()

outdir  = os.path.abspath(sys.argv[2].decode("utf-8"))
pl_name = sys.argv[1].decode("utf-8")

if not os.path.exists(outdir):
    print(u"directory: {} doesn't exist...".format(outdir))
    sys.exit()

print_header(u"Playlist: {}".format(pl_name))
sync_playlist(pl_name, outdir)
print_header(u"Sync of playlist {} complete!".format(pl_name))
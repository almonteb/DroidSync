# encoding: utf-8
###############################################################################
#
# Copyright 2010-2015 Brendan Almonte <almonteb@datawh.net>
# Portions of this software were developed by Dirk Ruediger <dirk@niebegeg.net>.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
###############################################################################

from __future__ import print_function
import os
import sys
import argparse
import shutil
from appscript import app

###############################################################################
# Misc Functions
###############################################################################

version = (1, 0, 0)
version_string = ".".join(map(str, version))

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
    print_header(u"Performing cleanup")
    for root, dirs, files in os.walk(directory):
        if u'.DS_Store' in files:
            os.remove(os.path.join(root, u'.DS_Store'))

    for root, dirs, files in os.walk(directory, True):
        if len(dirs) == 0 and len(files) == 0:
            print(u'Remove dir {}'.format(root))
            os.removedirs(root)

def sync_playlist(playlist_names, target_directory, add_only=False):
    # iTunes integration taken from
    # http://www.math.columbia.edu/%7Ebayer/Python/iTunes/
    files_in_playlists = []
    print_header(u"Collecting tracks")
    for playlist in app('iTunes').user_playlists():
        if playlist.name() in playlist_names:
            print(u'Include playlist "{}"'.format(playlist.name()))
            for t in playlist.file_tracks():
                files_in_playlists.append(t.location().path)

    itunes_music_folder = os.path.commonprefix(files_in_playlists)
    files_in_playlists = \
        [f.replace(itunes_music_folder, '') for f in files_in_playlists]
    files_on_droid = get_relative_filenames(target_directory)

    to_be_copied = [x for x in files_in_playlists if x not in files_on_droid]
    to_be_removed = [x for x in files_on_droid if x not in files_in_playlists]
    to_be_ignored = []

    files_on_both_sides = [x for x in files_in_playlists if x in files_on_droid]
    for f in files_on_both_sides:
        if os.path.getmtime(os.path.join(itunes_music_folder, f)) > \
            os.path.getmtime(os.path.join(target_directory, f)):
            to_be_copied.append(f)
        else:
            to_be_ignored.append(f)

    print_header(u"Ignoring tracks found on droid and in playlist")
    if len(to_be_ignored):
        for f in to_be_ignored:
            print(u'Ignore "{}"'.format(f))
    else:
        print(u"Nothing to ignore.")

    print_header(u"Copying tracks found in playlist, but not (or older) on droid")
    if len(to_be_copied):
        for f in sorted(to_be_copied):
            print(u'Copy "{}"'.format(f))
            target_dirname = os.path.join(target_directory, os.path.dirname(f))
            if not os.path.exists(target_dirname):
                os.makedirs(target_dirname)
            shutil.copy2(os.path.join(itunes_music_folder, f), target_dirname)
    else:
        print(u"Nothing to copy.")

    if add_only:
        print(u"Skip removing files.")
    else:
        print_header(u"Removing tracks found on droid, but not in playlist")
        if len(to_be_removed):
            for f in sorted(to_be_removed):
                print(u'Remove "{}"'.format(f))
                os.remove(os.path.join(target_directory, f))
        else:
            print(u"Nothing to remove.")

    clean_droid_dir(target_directory)


def unicode_safe(s):
    PY2K = sys.version_info[0] == 2
    if PY2K:
        return s.decode("utf-8")
    else:
        return s


def parse_args():
    description = '''
Copy music files from iTunes to an android device.
'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('-a', '--add', dest='add_only', action='store_const',
                        const=True, default=False,
                        help='only add files to target dir')
    parser.add_argument('playlist', nargs='+', help='the playlist name(s)')
    parser.add_argument('outdir', help='the target folder')
    return parser.parse_args()

###############################################################################
# Main
###############################################################################

def run_main():
    args = parse_args()
    outdir = os.path.abspath(unicode_safe(args.outdir))

    if not os.path.exists(outdir):
        print(u"directory {} doesn't exist...".format(outdir))
        sys.exit()

    pl_names = []
    for name in args.playlist:
        pl_names.append(unicode_safe(name))

    print_header(u"Playlists: {}".format(', '.join(pl_names)))
    sync_playlist(pl_names, outdir, add_only=args.add_only)
    print_header(u"Sync of playlists complete!")

if __name__ == 'main':
    run_main()
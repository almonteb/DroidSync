# DroidSync

A script to sync a playlist from iTunes with a folder (on your Android phone).
Currently it needs the target folder mounted as USB mass storage.

## Installation

Clone the project from GitHub and install it:

    git clone git://github.com/almonteb/DroidSync.git
    cd /path/to/project/DroidSync
    pip install -r requirements.txt
    python setup.py install

Enjoy!

## Usage

Call the script `droidsync` and define all iTunes playlists you want to clone
to your external device as well as the target folder (the mounted storage) as
arguments. Every argument except the last are interpreted as playlist names.
All media files in the target folder, that are not referenced in the playlist,
will be removed from your mobile device per default. If you add the option `-a`,
then no files are removed from the target folder.
Files, which are in the target folder, but are newer in your iTunes mediathek,
will be updated.

Examples:

- Copy all tracks from iTunes playlists "Droid" and "My party mix" to the folder
  `/Volumes/Droid/Music` and remove all files from the target folder, that are
  not part of any playlist.

        droidsync Droid "My party mix" /Volumes/Droid/Music

- Copy all tracks from iTunes playlist "My party mix" to the folder
  `/Volumes/Droid/Music` and leave all files in the target folder as they are.

        droidsync -a "My party mix" /Volumes/Droid/Music

## Contributors

- Brendan Almonte (almonteb@datawh.net) - Current maintainer
- Dave Bayer (https://www.math.columbia.edu/~bayer/Python/iTunes/),
  he has written the iTunes integration Code.
- Dirk Ruediger (dirk@niebegeg.net) made the script py3k compatible and
  converted into a deployable Pypi project

Feel free to fork, make changes and send a pull request.

## License

Copyright 2010-2015 Brendan Almonte <almonteb@datawh.net>
Portions of this software were developed by Dirk Ruediger <dirk@niebegeg.net>.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

   http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

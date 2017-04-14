#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import sys
import zipfile

import schedule
from spotify_ripper.progress import Progress
from spotify_ripper.ripper import Ripper
from spotify_ripper.utils import *
from frontend.my_app import app
from frontend.models import Setting, Rip, Song
import shutil


rip = Rip.query.filter(Rip.status == 1).first()

if not rip:
    exit()

rip_id = rip.id
print "New rip found - Id # %s" % rip_id


class DefaultArgs(object):
    aac = False
    aiff = False
    alac = False
    all_artists = False
    artist_album_market = None
    artist_album_type = None
    ascii = False
    ascii_path_only = False
    bitrate = u'320'
    cbr = False
    comment = None
    comp = u'10'
    cover_file = None
    cover_file_and_embed = None
    directory = None
    fail_log = None
    flac = False
    flat = False
    flat_with_index = False
    format_case = None
    genres = None
    grouping = None
    has_log = False
    id3_v23 = False
    large_cover_art = False
    last = False
    log = None
    mp4 = False
    normalize = False
    normalized_ascii = False
    opus = False
    output_type = u'mp3'
    overwrite = False
    partial_check = u'weak'
    pcm = False
    play_token_resume = None
    playlist_m3u = False
    playlist_sync = False
    playlist_wpl = False
    plus_pcm = False
    plus_wav = False
    quality = u'320'
    remove_from_playlist = False
    remove_offline_cache = False
    replace = None
    resume_after = None
    settings = None
    stereo_mode = None
    stop_after = None
    strip_colors = False
    timeout = None
    vbr = u'0'
    vorbis = False
    wav = False
    windows_safe = False


class MyRipper(Ripper):
    def load_track(self, idx, track):
        args = self.args
        track_tags = get_current_track_details(self, args.format.strip(), idx, track)
        # Check if file is in DB before adding to tracks list
        audio_file = self.format_track_path(idx, track)
        self.all_tracks.append((track, audio_file))
        Song.create_from_track_tags(track_tags, rip_id)

    def finish_rip(self, track):
        super(MyRipper, self).finish_rip(track)
        ## update song - rip complete


class MyProgress(Progress):
    def eta_calc(self):
        super(MyProgress, self).eta_calc()
        rip = Rip.query.get(rip_id)
        rip.total_duration = self.total_duration
        rip.total_position = self.total_position
        rip.song_duration = self.song_duration
        rip.song_position = self.song_position
        rip.song_eta = self.song_eta
        rip.total_eta = self.total_eta
        rip.save()


def zip_and_delete(folder_path, output_path):
    """Zip the contents of an entire folder (with that folder included
    in the archive). Empty subfolders will be included in the archive
    as well.
    """
    parent_folder = os.path.dirname(folder_path)
    # Retrieve the paths of the folder contents.
    contents = os.walk(folder_path)
    zipped_files = []
    try:
        zip_file = zipfile.ZipFile(output_path, 'w', zipfile.ZIP_DEFLATED)
        for root, folders, files in contents:
            # Include all subfolders, including empty ones.
            for folder_name in folders:
                absolute_path = os.path.join(root, folder_name)
                relative_path = absolute_path.replace(folder_path + '/',
                                                      '')
                print "Adding '%s' to archive." % absolute_path
                zip_file.write(absolute_path, relative_path)
            for file_name in files:
                absolute_path = os.path.join(root, file_name)
                relative_path = absolute_path.replace(folder_path + '/',
                                                      '')
                print "Adding '%s' to archive." % absolute_path
                zip_file.write(absolute_path, relative_path)
                zipped_files.append(absolute_path)
        print "'%s' created successfully." % output_path
    except IOError, message:
        print message
        sys.exit(1)
    except OSError, message:
        print message
        sys.exit(1)
    except zipfile.BadZipfile, message:
        print message
        sys.exit(1)
    finally:
        zip_file.close()

    print "clearing directory: %s" % folder_path
    shutil.rmtree(folder_path)
    os.mkdir(folder_path)

def main(prog_args=sys.argv[1:]):


    ####################
    #     Settings     #
    ####################

    class MyArgs(DefaultArgs):
        uri = rip.urls.split("\r\n")
        user = Setting.get("username")
        password = Setting.get("password")
        key = app.spotify_key_path
        format = 'frontend/songs/rips/'+Setting.get("format_string")

    ####################
    #     Rip Songs    #
    ####################


    args = MyArgs()
    rip.update_status(2)
    init_util_globals(args)
    try:
        ripper = MyRipper(args, MyProgress)
    except:
        print "Error Initializing Ripper.  Probably a bad app key"
        e = sys.exc_info()[0]
        print e
        rip.update_status(6)
        return
    ripper.start()
    # validate logged in and parse URIs
    if not ripper.login():
        rip.update_status(5)
        return
    else:
        ripper.ripper_continue.set()

    # Rip songs
    while ripper.isAlive():
        schedule.run_pending()
        ripper.join(0.1)

    zip_and_delete( "/app/spotify-ripper-simple/frontend/songs/rips",
                    "/app/spotify-ripper-simple/frontend/songs/zips/%s"%rip.file_name)

    rip.update_status(3)



if __name__ == '__main__':
    main()
"""
copy images to folder based on EXIT date

usage: python copy_photos.py /path/to/source/

requirements:
    python3
    arrow
    exifread
    pymediainfo -- mediainfo
"""

from concurrent.futures import ThreadPoolExecutor
from datetime import date, datetime
from shutil import copy
import os
import sys

from pymediainfo import MediaInfo
import arrow
import exifread


DIR_FORMAT = '%Y-%m-%d'
BASE_DIR = '/Volumes/OSXDATA/Pictures/Masters/'
VIDEO_DIR = '/Volumes/OSXDATA/Pictures/Videos/'
NODATE_DIR = '{}{}/'.format(BASE_DIR, 'nodate')


def is_movie(name):
    return any([
        name.upper().endswith('AVI'),
        name.upper().endswith('MOV'),
        name.upper().endswith('MP4'),
    ])


def is_image(name):
    return any([
        name.upper().endswith('JPG'),
        name.upper().endswith('JPEG'),
        name.upper().endswith('PNG'),
        name.upper().endswith('TIFF'),
        name.upper().endswith('GIF'),
    ])


def process_movie(root, name):
    nodate_dir = "{}{}/".format(VIDEO_DIR, 'nodate')
    path = "{}/{}".format(root, name)

    dt = get_movie_date(path)
    if dt:
        newdir = "{}{}/".format(VIDEO_DIR, dt.strftime(DIR_FORMAT))
        if not os.path.isdir(newdir):
            os.mkdir(newdir)

        newpath = "{}{}".format(newdir, name)
    else:
        newpath = "{}{}".format(nodate_dir, name)

    if not os.path.exists(newpath):
        print(path, newpath)
        copy(path, newpath)


def process_image(root, name):
    path = "{}/{}".format(root, name)
    dt = get_date(path)
    if dt:
        newdir = "{}{}/".format(BASE_DIR, dt.strftime(DIR_FORMAT))
        if not os.path.isdir(newdir):
            os.mkdir(newdir)

        newpath = "{}{}".format(newdir, name)
    else:
        newpath = "{}{}".format(NODATE_DIR, name)

    if not os.path.exists(newpath):
        print(path, newpath)
        copy(path, newpath)


def main(argv):
    path = argv[1]
    for root, dirs, files in os.walk(path):
        for name in files:
            if is_movie(name):
                with ThreadPoolExecutor(max_workers=4) as e:
                    process_movie(root, name)
            elif is_image(name):
                with ThreadPoolExecutor(max_workers=4) as e:
                    process_image(root, name)


def parse_date(date_str):
    dt, tm = date_str.split(' ')
    date_args = dt.split(':')
    date_args = map(int, date_args)

    time_args = tm.split(':')
    time_args = map(int, time_args)
    datetime_args = list(date_args) + list(time_args)
    return arrow.get(datetime(*datetime_args), 'Asia/Jakarta')


def get_date(name):
    with open(name, 'rb') as f:
        try:
            tags = exifread.process_file(f)
            datetime_keys = filter(lambda x: 'DATETIME' in x.upper(), tags.keys())

            dates = [tags.get(key) for key in datetime_keys]
            dates = filter(None, dates)
            dates = [parse_date(str(dt)) for dt in dates]
            if not dates:
                return None

            return min(dates)
        except:
            pass
    return None


def parse_movie_date(dt):
    dt = dt.replace('UTC', '')
    return arrow.get(dt.strip(), 'YYYY-MM-DD HH:mm:ss').to('Asia/Jakarta')


def get_movie_date(path):
    media_info = MediaInfo.parse(path)
    for track in media_info.tracks:
        dt = track.encoded_date
        if dt:
            return parse_movie_date(dt)

    return None

if __name__ == "__main__":
    main(sys.argv)

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


DIR_FORMAT = "%Y-%m-%d"
PICTURE_DIR = "/media/aldi/DATA/Pictures/"
BASE_DIR = "{}Masters/".format(PICTURE_DIR)
VIDEO_DIR = "{}Videos/".format(PICTURE_DIR)
NODATE_DIR = "{}{}/".format(BASE_DIR, "nodate")
FILE_FORMAT = "%Y%m%d%H%M%S%f"


def is_movie(name):
    return any(
        [
            name.upper().endswith("AVI"),
            name.upper().endswith("MOV"),
            name.upper().endswith("MP4"),
        ]
    )


def is_image(name):
    return any(
        [
            name.upper().endswith("JPG"),
            name.upper().endswith("JPEG"),
            name.upper().endswith("PNG"),
            name.upper().endswith("TIFF"),
            name.upper().endswith("GIF"),
        ]
    )


def get_new_name(dt, name):
    if dt:
        name_prefix = dt.strftime(FILE_FORMAT)
    else:
        name_prefix = "00000000000000"

    if name.startswith(name_prefix):
        name_prefix = ""
    else:
        name_prefix = "{}_".format(name_prefix)

    name = name.replace("NONAME_", "")
    new_name = "{}{}".format(name_prefix, name)
    return new_name


def process_movie(root, name):
    nodate_dir = "{}{}/".format(VIDEO_DIR, "nodate")
    path = "{}/{}".format(root, name)
    dt = get_movie_date(path)
    new_name = get_new_name(dt, name)

    if dt:
        newdir = "{}{}/".format(VIDEO_DIR, dt.strftime(DIR_FORMAT))
        if not os.path.isdir(newdir):
            os.mkdir(newdir)
        newpath = "{}{}".format(newdir, new_name)
    else:
        newpath = "{}{}".format(nodate_dir, new_name)

    if not os.path.exists(newpath):
        print(path, newpath)
        copy(path, newpath)


def process_image(root, name):
    path = "{}/{}".format(root, name)
    dt = get_date(path)
    new_name = get_new_name(dt, name)

    if dt:
        newdir = "{}{}/".format(BASE_DIR, dt.strftime(DIR_FORMAT))
        if not os.path.isdir(newdir):
            os.mkdir(newdir)

        newpath = "{}{}".format(newdir, new_name)
    else:
        newpath = "{}{}".format(NODATE_DIR, new_name)

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
    dt, tm = date_str.split(" ")
    date_args = dt.split(":")
    date_args = map(int, date_args)

    time_args = tm.split(":")
    time_args = map(int, time_args)
    datetime_args = list(date_args) + list(time_args)
    return arrow.get(datetime(*datetime_args), "Asia/Jakarta")


def get_date(name):
    dt = None
    with open(name, "rb") as f:
        try:
            tags = exifread.process_file(f)
            datetime_keys = filter(lambda x: "DATETIME" in x.upper(), tags.keys())

            dates = [tags.get(key) for key in datetime_keys]
            dates = filter(None, dates)
            dates = [parse_date(str(dt)) for dt in dates]
            if dates:
                return min(dates)

        except:
            pass

    # if not dt:
    #     created_time = datetime.fromtimestamp(os.path.getctime(name))
    #     dt = arrow.get(created_time, 'Asia/Jakarta')
    return dt


def parse_movie_date(dt):
    dt = dt.replace("UTC", "")
    return arrow.get(dt.strip(), "YYYY-MM-DD HH:mm:ss").to("Asia/Jakarta")


def get_movie_date(path):
    dt = None
    media_info = MediaInfo.parse(path)
    for track in media_info.tracks:
        dt = track.encoded_date
        if dt:
            return parse_movie_date(dt)

    # created_time = datetime.fromtimestamp(os.path.getctime(path))
    # dt = arrow.get(created_time, 'Asia/Jakarta')
    return dt


if __name__ == "__main__":
    if not sys.argv:
        print("python copy_photos.py ./")
    else:
        main(sys.argv)

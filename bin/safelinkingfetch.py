#!/usr/bin/env python
import requests
import sys


def fetch(filename):
    with open(filename, "rb") as f:

        for line in f.readlines():

            if line.startswith("#"):
                continue

            r = requests.get(line.strip(), allow_redirects=False)
            location = r.headers.get('location')
            url = location.split('?', 1)[1]
            sys.stdout.write(url + "\n")

if __name__ == "__main__":

    filename = sys.argv[1]
    fetch(filename)

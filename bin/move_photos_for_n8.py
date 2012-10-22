#!/usr/bin/env python
import os


def main():
    """
    Moves yyyy-mm-dd-xxx.jpg file to yyy-mm-dd folder.
    """
    for root, dirs, files in os.walk("."):
        for single in files:

            if single.endswith(".py"):
                continue

            if not os.path.isfile(single):
                continue

            dirname = single.rsplit("-", 1)[0]

            if not os.path.isdir(dirname):
                os.mkdir(dirname)

            newlocation = "{dirname}/{filename}".format(
                dirname=dirname, filename=single)

            os.rename(single, newlocation)

if __name__ == "__main__":
    main()

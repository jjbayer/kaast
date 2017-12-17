#!/usr/bin/env python
import argparse
import sys
from time import sleep

from pychromecast import get_chromecasts

from caster import Caster


def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('filename')
    args = parser.parse_args(sys.argv[1:])

    print("Looking for chromecast devices ... ")
    chromecasts = get_chromecasts()
    if not chromecasts:
        print("No chromecasts found")
        sys.exit(1)
    else:
        chromecast = chromecasts[0]
        print("Found %s at %s" % (
            chromecast.name, chromecast.host))

        caster = Caster(chromecast)

        caster.play_media(args.filename)

        sleep(60*60*24)

if __name__ == '__main__':
    main()

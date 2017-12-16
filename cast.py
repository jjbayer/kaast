import argparse
import sys
import http.server
import socketserver
from time import sleep
from tempfile import TemporaryDirectory
import os
import threading
import random
import mimetypes

from pychromecast import get_chromecasts
import netifaces


PORT = random.randint(8700, 8800)


class UnsupportedMimeType(RuntimeError):

    pass


def get_own_ip():

    _, interface = netifaces.gateways()['default'][netifaces.AF_INET]
    
    return netifaces.ifaddresses(interface)[netifaces.AF_INET][0]['addr']
    

class SingleFileWebServer:

    def  __init__(self, filename):

        self._filename = filename
        self.content_type = mimetypes.guess_type(filename)[0]

        self._pseudoname = (
            "video%s" % mimetypes.guess_extension(self.content_type)
        )

    def __enter__(self):

        self._tempdir = TemporaryDirectory()
        self._tempdir.__enter__()
        dir_ = self._tempdir.name
        symlink_target = os.path.join(dir_, self._pseudoname)
        os.symlink(self._filename, symlink_target)
        os.chdir(self._tempdir.name)

        Handler = http.server.SimpleHTTPRequestHandler

        self._httpd = socketserver.TCPServer(
            ("", PORT), Handler)

        print("serving at port", PORT)
        threading._start_new_thread(
            self._httpd.serve_forever, ())
        
        self.url = "http://%s:%s/%s" %(get_own_ip(), PORT, self._pseudoname)
        print(self.url)

        return self

    def __exit__(self, *args, **kwargs):

        self._httpd.shutdown()
        self._tempdir.__exit__(*args, **kwargs)



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
        
        play_media(chromecast, args.filename)


def play_media(chromecast, filename):
    
    chromecast.wait()
    mc = chromecast.media_controller

    with SingleFileWebServer(filename) as server:

        print("File should be available at %s" % server.url)

        # mc.play_media(
        #     server.url,
        #     content_type=server.content_type)
        # mc.block_until_active()
        # print(mc.status)

        # sleep(10)

if __name__ == '__main__':
    main()
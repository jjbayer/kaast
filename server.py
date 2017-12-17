import http.server
import mimetypes
import os
import random
import socketserver
from tempfile import TemporaryDirectory
import threading

from network import get_own_ip


PORT = random.randint(8700, 8800)


class SingleFileWebServer:

    def __init__(self, filename):

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

        print("Stopping web server...")
        self._httpd.shutdown()
        print("Removing tempdir...")
        self._tempdir.__exit__(*args, **kwargs)
        print("Done.")

import pychromecast

from server import SingleFileWebServer


class Caster:

    def __init__(self, chromecast: pychromecast.Chromecast):
        self._chromecast = chromecast
        self._media_controller = chromecast.media_controller

    def play_media(self, filename):

        with SingleFileWebServer(filename) as server:

            print("File should be available at %s" % server.url)
            # mc.play_media(
            #     server.url,
            #     content_type=server.content_type)
            # mc.block_until_active()
            # print(mc.status)


    def play(self):
        pass

    def pause(self):
        pass

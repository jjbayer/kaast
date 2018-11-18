import pychromecast

from server import SingleFileWebServer


class Caster:

    def __init__(self, chromecast: pychromecast.Chromecast):
        self._chromecast = chromecast
        self._media_controller = chromecast.media_controller
        self._server = None

    def play_media(self, filename):

        server = self._server = SingleFileWebServer(filename).__enter__()
        print(
            "File should be available at %s, content type %s"
            % (server.url, server.content_type))
        self._media_controller.play_media(
            server.url,
            content_type=server.content_type)

    def play(self):
        self._media_controller.play()

    def pause(self):
        self._media_controller.pause()

    def stop(self):
        self._media_controller.stop()
        self._server.__exit__(None, None, None)
        self._server = None

    @property
    def name(self):
        return self._chromecast.name

from pathlib import Path
from urllib.parse import urlencode
import logging
import os

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse

from pychromecast import get_chromecasts
from caster import Caster


LOG = logging.getLogger(__name__)


def index(request, path=None):

    abs_path, is_root = get_path(path)

    files = list(os.scandir(str(abs_path)))

    return render(request, 'index.pug', {
        'directory': [
            {
                'is_dir': entry.is_dir(),
                'rel_path': ("%s/%s" % (path, entry.name)) if path else entry.name,
                'name': entry.name
            }
            for entry in os.scandir(str(abs_path))
        ],
        'is_root': is_root,
    })


def file(request, path):

    abs_path, _ = get_path(path)
    assert abs_path.is_file()

    parent = abs_path.parent
    rel_path_parent = parent.relative_to(settings.MEDIA_DIRECTORY)

    state = None
    action = request.GET.get('action')
    if action == "start":
        LOG.info("Try playing %s", abs_path)
        get_caster().play_media(str(abs_path))
        state = "playing"
    elif action == "pause":
        LOG.info("Try pausing %s", abs_path)
        get_caster().pause()
        state = "paused"
    elif action == "resume":
        LOG.info("Try resuming %s", abs_path)
        get_caster().play()
        state = "playing"
    elif action == "stop":
        LOG.info("Try to stop %s", abs_path)
        get_caster().stop()
        state = "stopped"

    return render(request, 'file.pug', {
        'parent': abs_path.parent.name,
        'parent_path': rel_path_parent,
        'name': abs_path.name,
        'state': state,
        'chromecast_name': get_caster().name,
    })

    
# def start(request):

#     abs_path, _ = get_path(request)

#     params = request.GET.copy()
#     params['state'] = 'playing'
#     params['path'] = abs_path.parent.relative_to(settings.MEDIA_DIRECTORY)
    
#     return redirect_with_params('index', params)



def get_path(rel_path):
    abs_path = Path(settings.MEDIA_DIRECTORY)
    is_root = True
    if rel_path:
        assert(".." not in rel_path)
        abs_path /= rel_path
        assert(abs_path.exists())
        is_root = False

    return abs_path, is_root


# def redirect_with_params(view_name, params):

#     return HttpResponseRedirect(url_with_params(view_name, params))


# def url_with_params(view_name, params):

#     return reverse(view_name) + "?" + urlencode(params)


def get_caster():

    if not hasattr(get_caster, '_caster'):
        get_caster._caster = Caster(get_chromecasts()[0])

    return get_caster._caster
from pathlib import Path
import os
from urllib.parse import urlencode

from django.conf import settings
from django.http import HttpResponseRedirect
from django.shortcuts import render, reverse


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

    return render(request, 'file.pug', {
        'name': abs_path.name
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
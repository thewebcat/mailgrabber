# -*- coding: UTF-8 -*-
import json
from functools import wraps

from decorator import decorator
from django.http import HttpResponse
from django.http.response import HttpResponseBadRequest
from django.shortcuts import render_to_response
from django.template import RequestContext


def ajax_required(f):
    """
    AJAX request required decorator
    use it in your views:

    @ajax_required
    def my_view(request):
        ....

    """
    def wrap(request, *args, **kwargs):
            if not request.is_ajax():
                return HttpResponseBadRequest()
            return f(request, *args, **kwargs)
    wrap.__doc__ = f.__doc__
    wrap.__name__ = f.__name__
    return wrap


@decorator
def render_to_json(func, request, *args, **kw):
    """
    Декоратор, который возвращает json

    Usage:
    @render_to_json
    def my_view(request, param):
        if param == 'something':
            return {'data': 'some_data'}
        else:
            return {'data': 'some_other_data'}
    """
    output = func(request, *args, **kw)
    if isinstance(output, dict):
        return HttpResponse(json.dumps(output), content_type='application/json; charset=UTF-8')
    else:
        return output


def render_to(template):
    """
    Decorator for Django views that sends returned dict to render_to_response function
    with given template and RequestContext as context instance.

    If view doesn't return dict then decorator simply returns output.
    Additionally view can return two-tuple, which must contain dict as first
    element and string with template name as second. This string will
    override template name, given as parameter

    Parameters:

     - template: template name to use

    url snippet https://djangosnippets.org/snippets/821/

    Usage:
    @render_to('my/template.html')
    def my_view(request, param):
        if param == 'something':
            return {'data': 'some_data'}
        else:
            return {'data': 'some_other_data'}, 'another/template.html'
    """
    def renderer(func):
        @wraps(func)
        def wrapper(request, *args, **kw):
            output = func(request, *args, **kw)
            if isinstance(output, (list, tuple)):
                return render_to_response(output[1], output[0], RequestContext(request))
            elif isinstance(output, dict):
                return render_to_response(template, output, RequestContext(request))
            return output
        return wrapper
    return renderer


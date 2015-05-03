# import datetime
import json
# import os

# from django.conf import settings
from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response


def render_to_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="application/json", status=status, mimetype='application/json')


def global_render_to_response(template, render_data):
    return render_to_response(template, render_data)


def home(request):
    render_data = {}
    return global_render_to_response("index.html", render_data)

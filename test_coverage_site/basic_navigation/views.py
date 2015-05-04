import datetime
import json
# import os

# from django.conf import settings
from django.http import HttpResponse
# from django.http import HttpResponseRedirect
# from django.http import HttpResponsePermanentRedirect
from django.shortcuts import render_to_response
from test_coverage_site.scoreboard.models import ScoreBoard


def render_to_json(data, status=200):
    return HttpResponse(json.dumps(data), content_type="application/json", status=status, mimetype='application/json')


def global_render_to_response(template, render_data):
    return render_to_response(template, render_data)


def home(request):
    render_data = {}
    return global_render_to_response("index.html", render_data)


def show_project(request, project_identifier):
    score_board = ScoreBoard.get_latest(project_identifier)
    render_data = {
        "score_board": score_board
    }
    return global_render_to_response("project.html", render_data)


def show_project_on_date(request, project_identifier, year, month, day):
    year, month, day = [int(item) for item in (year, month, day)]
    date = datetime.date(year=year, month=month, day=day)
    score_board = ScoreBoard.get_on_date(project_identifier, date)
    render_data = {
        "score_board": score_board
    }
    return global_render_to_response("project.html", render_data)

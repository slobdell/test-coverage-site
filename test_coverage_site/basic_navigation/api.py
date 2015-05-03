import json

from django.http import Http404
from django.http import HttpResponse

from test_coverage_site.scoreboard.models import ScoreBoard


def render_to_json(response_obj, context={}, content_type="application/json", status=200):
    json_str = json.dumps(response_obj, indent=4)
    return HttpResponse(json_str, content_type=content_type, status=status)


def requires_post(fn):
    def inner(request, *args, **kwargs):
        if request.method != "POST":
            return Http404
        post_data = request.POST or json.loads(request.body)
        kwargs["post_data"] = post_data
        return fn(request, *args, **kwargs)
    return inner


@requires_post
def save_score(request, project_identifier, post_data=None):
    score_board = ScoreBoard.get_or_create(project_identifier)
    score_board.save_data(post_data)
    return render_to_json({}, status=204)

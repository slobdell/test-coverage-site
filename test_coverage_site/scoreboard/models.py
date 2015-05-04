import datetime
import json

from django.core.exceptions import ObjectDoesNotExist
from django.db import models


class _ScoreBoard(models.Model):
    project_name = models.CharField(max_length=255)
    date = models.DateField()
    json_data = models.TextField(default="{}")

    class Meta:
        index_together = [
            ("project_name", "date"),
        ]


class ScoreBoard(object):

    def __init__(self, _scoreboard):
        self._scoreboard = _scoreboard

    @classmethod
    def get_or_create(cls, project_name, date=None):
        date = date or datetime.datetime.utcnow().date()
        try:
            _scoreboard = _ScoreBoard.objects.get(project_name=project_name, date=date)
        except ObjectDoesNotExist:
            _scoreboard = _ScoreBoard.objects.create(
                project_name=project_name,
                date=date
            )
        return cls(_scoreboard)

    @classmethod
    def get_latest(cls, project_name):
        try:
            _scoreboard = _ScoreBoard.objects.filter(project_name="test_run").latest("date")
        except ObjectDoesNotExist:
            pass  # SBL FIXME USE NULL OBJECT PATTERN
        return cls(_scoreboard)

    @classmethod
    def get_on_date(cls, project_name, date):
        try:
            _scoreboard = _ScoreBoard.objects.filter(
                project_name="test_run",
                date__lte=date
            ).latest("date")
        except ObjectDoesNotExist:
            pass  # SBL FIXME USE NULL OBJECT PATTERN
        return cls(_scoreboard)

    def save_data(self, json_data):
        self._scoreboard.json_data = json.dumps(json_data)
        self._scoreboard.save()

    @property
    def formatted_tuples(self):
        json_dict = json.loads(self._scoreboard.json_data)
        ranked_rows = sorted(json_dict["test_coverage"].items(), key=lambda t: t[1], reverse=True)
        for index in xrange(len(ranked_rows)):
            author, score = ranked_rows[index]
            score *= 100.0
            line_count = json_dict["line_counts"][author]
            ranked_rows[index] = (author, score, line_count,)
        return ranked_rows

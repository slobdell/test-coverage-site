import datetime
import json
import sys

from django.core.exceptions import ObjectDoesNotExist
from django.db import models

DEFAULT_MIN_AUTHORS = 5
DEFAULT_DISPLAY_PERCENT = 0.3


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
            _scoreboard = _ScoreBoard.objects.filter(project_name=project_name).latest("date")
        except ObjectDoesNotExist:
            pass  # SBL FIXME USE NULL OBJECT PATTERN
        return cls(_scoreboard)

    @classmethod
    def get_on_date(cls, project_name, date):
        try:
            _scoreboard = _ScoreBoard.objects.filter(
                project_name=project_name,
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
            display_line_count = self._format_line_count(line_count)
            ranked_rows[index] = (author, score, display_line_count)

        ranked_rows = self._truncate_rows(ranked_rows)
        return ranked_rows

    def _format_line_count(self, line_count):
        thresh_to_str = {
            500: "Fewer Than 500 lines",
            10000: "500 to 10,000 lines",
            sys.maxint: "Greater than 10,000 lines",
        }
        for thresh, display_str in sorted(thresh_to_str.items(), key=lambda t: t[0]):
            if line_count < thresh:
                return display_str

    def _truncate_rows(self, ranked_rows):
        json_dict = json.loads(self._scoreboard.json_data)  # TODO: cache that value

        min_authors = json_dict.get("min_authors", DEFAULT_MIN_AUTHORS)
        display_percent = json_dict.get("display_percent", DEFAULT_DISPLAY_PERCENT)
        cutoff_count = max(int(len(ranked_rows) * display_percent), min_authors)
        return ranked_rows[:cutoff_count]

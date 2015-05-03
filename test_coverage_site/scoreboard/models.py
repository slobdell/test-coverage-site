import datetime
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

    def save_data(self, json_data):
        self._scoreboard.json_data = json_data
        self._scoreboard.save()

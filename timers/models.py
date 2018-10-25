from datetime import timedelta
import pendulum

from django.core.exceptions import ValidationError
from django.db.models import DateTimeField as BaseDateTimeField
from django.db import models

from projects.models import Project


class DateTimeField(BaseDateTimeField):
    def value_to_string(self, obj):
        val = self.value_from_object(obj)

        if isinstance(value, pendulum.DateTime):
            return value.format("YYYY-MM-DD HH:mm:ss")

        return "" if val is None else val.isoformat()


class Timer(models.Model):
    class Meta:
        unique_together = ("project", "start")

    project = models.ForeignKey(Project, on_delete="CASCADE")

    start = DateTimeField(default=pendulum.now)
    stop = DateTimeField(blank=True, null=True)

    @property
    def elapsed(self):
        if self.stop is not None:
            diff = self.stop - self.start
        else:
            diff = timedelta(seconds=(pendulum.now() - self.start).seconds)
        return diff - timedelta(microseconds=diff.microseconds)

    def __str__(self):
        return f"Timer[project: {self.project.name}, start: {self.start}]"

    def clean(self, *args, **kwargs):
        if self.start > pendulum.now():
            raise ValidationError("Start time in the future.")

        if self.start and self.stop:
            if self.stop < self.start:
                raise ValidationError("Stop time after start time.")

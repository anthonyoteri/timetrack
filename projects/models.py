from datetime import datetime

from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    class Meta:
        unique_together = ("slug", "user")

    name = models.CharField(max_length=64)
    slug = models.SlugField()
    description = models.CharField(max_length=255, blank=True)

    archived = models.BooleanField(default=False)
    favorite = models.BooleanField(default=False)

    user = models.ForeignKey(User, default=None, on_delete="CASCADE")

    created = models.DateTimeField(default=datetime.now)
    last_updated = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    @property
    def last_used(self):
        candidates = [t.start for t in self.timer_set.all()]
        if not candidates:
            return None

        return max(candidates).date()

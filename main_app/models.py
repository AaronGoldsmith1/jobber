from django.db import models

from django.contrib.auth.models import User

EVENT_TYPES = (
    ('T', 'Technology'),
    ('M', 'Marketing'),
    ('N', 'Networking'),
    ('C', 'Career')
)


class Event(models.Model):
    title = models.CharField(max_length=250, null=False)
    dateTime = models.DateTimeField(null=False)
    speaker = models.CharField(max_length=250, null=False)
    description = models.CharField(max_length=350, null=False)
    category = models.CharField(
        max_length=1,
        choices=EVENT_TYPES,
        default=EVENT_TYPES[0][0]
    )
    users = models.ManyToManyField(User, blank=True)

    def __str__(self):
        return self.title

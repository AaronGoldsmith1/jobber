from django.db import models

from django.contrib.auth.models import User

EVENT_TYPES = (
    ('T', 'Technology'),
    ('M', 'Marketing'),
    ('N', 'Networking'),
    ('C', 'Career')
)


class Event(models.Model):
    title = models.CharField(max_length=250)
    dateTime = models.DateTimeField()
    speaker = models.CharField(max_length=250)
    description = models.CharField(max_length=350)
    type = models.CharField(
        max_length=1,
        choices=EVENT_TYPES,
        default=EVENT_TYPES[0][0]
    )
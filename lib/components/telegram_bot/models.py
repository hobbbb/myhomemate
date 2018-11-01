from django.db import models


class TelegrmaBotPollingCommand(models.Model):
    TYPE_CHOICES = [
        ('script', u'Script')
    ]

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=15, choices=TYPE_CHOICES)
    command = models.CharField(max_length=50)
    body = models.TextField()

from django.db import models
from django.apps import apps
from django.utils import timezone


class CommonAbstractModel(models.Model):
    created_date = models.DateTimeField(null=True, auto_now_add=True)
    updated_date = models.DateTimeField(null=True, auto_now=True)
    status = models.BooleanField(default=True)

    class Meta:
        abstract = True
from django.contrib.auth.models import User
from django.db import models

from rest_framework.fields import HStoreField


class UserPreference(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    texture_preferences = HStoreField(null=True, blank=True)
    scent_preferences = HStoreField(null=True, blank=True)

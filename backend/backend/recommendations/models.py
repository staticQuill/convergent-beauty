from django.contrib.auth.models import User
from django.contrib.postgres.fields import HStoreField
from django.db import models



class UserPreference(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    texture_preferences = HStoreField(null=True, blank=True)
    scent_preferences = HStoreField(null=True, blank=True)

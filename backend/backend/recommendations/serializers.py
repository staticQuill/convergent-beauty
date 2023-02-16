from rest_framework import serializers

from .models import UserPreference


class UserPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserPreference
        fields = "__all__"
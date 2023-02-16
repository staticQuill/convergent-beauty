from rest_framework import serializers

from .models import UserPreference


class UserPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = UserPreference
        lookup_field = 'user'
        fields = "__all__"

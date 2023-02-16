from rest_framework import serializers

from .models import UserPreference
from auth.serializers import SimpleUserSerializer


class UserPreferenceSerializer(serializers.HyperlinkedModelSerializer):
    user = SimpleUserSerializer(read_only=True)

    class Meta:
        model = UserPreference
        lookup_field = 'user'
        fields = "__all__"

# Create your views here.
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from .models import UserPreference
from .serializers import UserPreferenceSerializer
from products.models import UserProduct


class UserPreferenceView(APIView):
    def get(self, request) -> Response:
        obj = UserPreference.objects.get(user=request.user)

        return Response(UserPreferenceSerializer(obj, context={'request': request}).data)

    def _total_sensory_values(self, current_preference: dict, total_loggings: int, personal: list, community: dict, modifier: int) -> dict:
        sensory_preferences = {}
        for sensory in personal:
            try:
                sensory_preferences[str(sensory)] += 4 * modifier
            except KeyError:
                sensory_preferences[str(sensory)] = 4 * modifier
        for sensory_key, value in community.items():
            weight = int(value) / total_loggings
            try:
                sensory_preferences[str(sensory_key)] += 2 * modifier * weight
            except KeyError:
                sensory_preferences[str(sensory_key)] = 2 * modifier * weight
        return sensory_preferences

    def _generate_modifier(self, enjoyment: list) -> int:
        if "neutral" in enjoyment or ("unpleasant" in enjoyment and "pleasant" in enjoyment):
            return 0
        elif "unpleasant" in enjoyment:
            return -1
        elif "pleasant" in enjoyment:
            return 1
        else:
            return 0

    def post(self, request) -> Response:
        user = request.user

        try:
            user_products = [product for product in UserProduct.objects.filter(user=user)]
        except ObjectDoesNotExist:
            return Response({"error": "User has no products yet!"}, status=HTTP_404_NOT_FOUND)

        texture_preferences = {}
        scent_preferences = {}
        for product in user_products:
            total_product_loggings = product.product.times_logged
            texture_modifier = self._generate_modifier(product.texture_enjoyment)
            personal_textures = product.texture_notes
            community_textures = product.product.texture_ratings
            texture_preferences = self._total_sensory_values(
                current_preference = texture_preferences,
                total_loggings=total_product_loggings,
                personal=personal_textures,
                community=community_textures,
                modifier=texture_modifier
            )
            scent_modifier = self._generate_modifier(product.scent_enjoyment)
            personal_scent = product.scent_notes
            community_scent = product.product.scent_ratings
            scent_preferences = self._total_sensory_values(
                current_preference = scent_preferences,
                total_loggings=total_product_loggings,
                personal=personal_scent,
                community=community_scent,
                modifier=scent_modifier
            )

        try:
            user_preference = UserPreference.objects.get(user=user)
            user_preference.texture_preferences = texture_preferences
            user_preference.scent_preferences = scent_preferences
        except ObjectDoesNotExist:
            user_preference = UserPreference(
                user=user,
                texture_preferences=texture_preferences,
                scent_preferences=scent_preferences
            )

        user_preference.save()

        return Response(UserPreferenceSerializer(user_preference, context={'request': request}).data, status=HTTP_200_OK)


# Create your views here.
from decimal import Decimal
from typing import List

from django.core.exceptions import ObjectDoesNotExist
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_200_OK
from rest_framework.views import APIView

from .models import UserPreference
from .serializers import UserPreferenceSerializer
from products.models import UserProduct
from search_engine.errors import ElasticsearchError

from search_engine.services import SearchService

from kink import inject


class UserPreferenceView(APIView):
    def get(self, request) -> Response:
        obj = UserPreference.objects.get(user=request.user)

        return Response(UserPreferenceSerializer(obj, context={'request': request}).data)

    def _total_sensory_values(self, preferences: dict, total_loggings: int, personal: list, community: dict, modifier: int) -> dict:
        for sensory in personal:
            try:
                preferences[str(sensory)] += 4 * modifier
            except KeyError:
                preferences[str(sensory)] = 4 * modifier
        for sensory_key, value in community.items():
            weight = int(value) / total_loggings
            try:
                preferences[str(sensory_key)] += 2 * modifier * weight
            except KeyError:
                preferences[str(sensory_key)] = 2 * modifier * weight
        return preferences

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
                preferences = texture_preferences,
                total_loggings=total_product_loggings,
                personal=personal_textures,
                community=community_textures,
                modifier=texture_modifier
            )
            scent_modifier = self._generate_modifier(product.scent_enjoyment)
            personal_scent = product.scent_notes
            community_scent = product.product.scent_ratings
            scent_preferences = self._total_sensory_values(
                preferences = scent_preferences,
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


@inject
class RecommendationView(APIView):
    def __init__(self, search_service: SearchService):
        self.search_service = search_service

    def _generate_sort_params(self, texture: dict, scent: dict) -> List[dict]:
        unsorted = []
        combined_preferences = {**texture, **scent}
        for k, v in combined_preferences.items():
            if k in texture:
                unsorted.append({"k": f"texture_ratings.{k}", "v": v, "path": "texture_ratings"})
            if k in scent:
                unsorted.append({"k": f"scent_ratings.{k}", "v": v,  "path": "scent_ratings"})

        return [{kv["k"]: {"unmapped_type": "integer", "missing": ("_last" if Decimal(kv["v"]) > 0 else "_first"), "order": ("asc" if Decimal(kv["v"]) > 0 else "desc"), "nested_path": kv["path"]}} for kv in sorted(unsorted, key=lambda d: abs(Decimal(d["v"])))][::-1]

    def get(self, request) -> Response:
        try:
            user_preference = UserPreference.objects.get(user=request.user)
        except ObjectDoesNotExist:
            return Response({"error": "User has not generated preferences yet!"}, status=HTTP_404_NOT_FOUND)

        sort_params = self._generate_sort_params(
            texture=user_preference.texture_preferences,
            scent=user_preference.scent_preferences
        )

        return Response(dict(self.search_service.get_recommendations(sort_list=sort_params)), status=HTTP_200_OK)
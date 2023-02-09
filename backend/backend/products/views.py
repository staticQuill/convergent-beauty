import json
from uuid import uuid4

from django.contrib.auth.models import AnonymousUser, User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from .models import Product, Brand, UserProduct
from .serializers import UserProductSerializer


class UserProductView(APIView):
    def get(self, request) -> Response:
        products = UserProduct.objects.all()

        return Response(UserProductSerializer(products).data)

    @staticmethod
    def _increment_product_ratings(
            ratings: dict,
            notes: list
    ) -> dict:
        # texture_notes takes the form like ["sticky", "wet"] etc,
        # just a list of attributes from one person's input
        for note in notes:
            if note in ratings.keys():
                ratings[note] += 1
            else:
                ratings[note] = 1
        return ratings

    def _alter_product_attributes(
            self,
            product: Product,
            texture_notes: list,
            scent_notes: list,
            sentiments: list
    ) -> None:
        product.texture_ratings = self._increment_product_ratings(ratings=product.texture_ratings, notes=texture_notes)
        product.scent_ratings = self._increment_product_ratings(ratings=product.scent_ratings, notes=scent_notes)
        product.sentiment_ratings = self._increment_product_ratings(ratings=product.sentiment_ratings, notes=sentiments)
        product.save()

    def post(self, request) -> Response:
        user = request.user
        request_body = json.loads(request.body)
        brand, _ = Brand.objects.get_or_create(name=request_body["brand_name"])
        product, _ = Product.objects.get_or_create(brand=brand.pk, name=request_body["product_name"])
        self._alter_product_attributes(product, request_body["texture_notes"], request_body["scent_notes"], request_body["sentiments"])
        new_user_product_id = str(uuid4())[:8]
        user_product = UserProduct(
            user_product_id=new_user_product_id,
            product=product,
            user=user,
            custom_notes=request_body["custom_notes"],
            texture_notes=[note for note in request_body["texture_notes"]],
            texture_enjoyment=[note for note in request_body["texture_enjoyment"]],
            scent_notes=[note for note in request_body["scent_notes"]],
            scent_enjoyment=[note for note in request_body["scent_enjoyment"]],
            overall_sentiments=[note for note in request_body["sentiments"]],
        )
        user_product.save()

        return Response(UserProductSerializer(user_product).data, status=HTTP_201_CREATED)

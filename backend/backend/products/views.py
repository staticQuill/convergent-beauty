import json
from uuid import uuid4

from django.contrib.auth.models import AnonymousUser, User
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED
from rest_framework.views import APIView

from backend.products.models import Product


class UserProductView(APIView):
    def get(self, request) -> Response:
        athletes = Product.objects.all()

        return Response(ProductSerializer(athletes).data)

    def post(self, request) -> Response:
        user = request.user
        new_product_id = str(uuid4())[:8]
        product = Product(product_id=new_product_id)
        product.save()

        return Response(ProductSerializer(product).data, status=HTTP_201_CREATED)

# Create your views here.

import logging

from kink import inject
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.views import APIView
from search_engine.services import SearchService

logger = logging.getLogger(__file__)


@inject
class SearchAutocompleteView(APIView):
    def __init__(self, search_service: SearchService):
        self.search_service = search_service

    def get(self, request) -> Response:
        field = request.GET.get("field", "brand")
        index = request.GET.get("type")
        partial = request.GET.get("partial")
        brand = ""
        if field == "product":
            brand = request.GET.get("brand")

        response = self.search_service.get_autocompletes(index=index, field=field, partial=partial, brand=brand)

        return Response(response, status=HTTP_200_OK)

import os
from typing import Protocol

from kink import inject

from elasticsearch import Elasticsearch, ApiError

from .errors import ElasticsearchError


@inject
class SearchClient():
    def __init__(self):
        elastic_password = os.getenv("ELASTIC_PASS")
        self.client = Elasticsearch(
            "http://localhost:9200",
            basic_auth=("elastic", elastic_password)
                               )

    def create(self, index: str, product: dict) -> None:
        try:
            self.client.create(index=index, document=product)
        except (ApiError) as e:
            raise ElasticsearchError(str(e))

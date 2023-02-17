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

    def create(self, index: str, id: str, product: dict) -> None:
        try:
            self.client.create(index=index, id=id, document=product)
        except (ApiError) as e:
            raise ElasticsearchError(str(e))

    def update(self, index: str, id: str, product: dict) -> None:
        try:
            self.client.update(index=index, id=id, doc=product)
        except (ApiError) as e:
            raise ElasticsearchError(str(e))

    def search(self, sort: list, index: str = "_all") -> list:
        return self.client.search(sort=sort, index=index)

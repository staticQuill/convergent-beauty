import os
from typing import Protocol

from elastic_transport import TransportError
from kink import inject

from elasticsearch import Elasticsearch, ApiError

from .errors import ElasticsearchError


class ISearchClient(Protocol):
    def create(self) -> None:
        ...


@inject(alias=ISearchClient)
class SearchClient(Protocol):
    def __init__(self):
        elastic_password = os.getenv("ELASTIC_PASS")
        self.client = Elasticsearch(
            "http://localhost:9200",
            basic_auth=("elastic", elastic_password)
                               )

    def create(self, index: str, product: dict) -> None:
        try:
            self.client.create(index=index, document=product)
        except (ApiError, TransportError) as e:
            raise ElasticsearchError(str(e))

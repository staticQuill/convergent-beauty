import os
from typing import Protocol, List

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

    def convert_index_to_alias(self, index: str) -> str:
        if "-" in index:
            index = index.split("-")[0]
        return index + "_alias"

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

    def search(self, sort: list, offset: int, index: str) -> list:
        return [result["_source"] for result in self.client.search(sort=sort, from_=offset, index=index)["hits"]["hits"]]

    def partial_search(self, field: str, partial: str, index: str, brand: str = None) -> List[dict]:
        query = {"nested": {"path": "brand", "query": {"match_phrase_prefix": {field: partial}}}}
        alias = self.convert_index_to_alias(index=index)
        if brand:
            query = {
                "bool": {
                    "must": [
                        {
                            "match_phrase_prefix": {
                                field: partial.lower()
                              }
                            }
                          ],
                    "filter": [
                        {
                            "nested": {
                                "path": "brand",
                                "query": {
                                    "match": {
                                        "brand.name": brand.lower()
                                    }
                                }
                            }
                        }
                    ]
                        }
                      }

        search_results = self.client.search(index=alias, query=query)
        return [result["_source"] for result in search_results["hits"]["hits"]]
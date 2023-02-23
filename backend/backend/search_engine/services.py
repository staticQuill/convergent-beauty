from typing import Protocol

from kink import inject

from .client import SearchClient


@inject
class SearchService():
    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    def add_serialized_product(self, new: bool, id: str, product: dict) -> None:
        index = product["type"]
        if new:
            self.search_client.create(index=index, id=id, product=product)
        else:
            self.search_client.update(index=index, id=id, product=product)

    def get_recommendations(self, sort_list: list, index: str = "*,-.*,-kibana") -> list:
        return self.search_client.search(sort=sort_list, index=index)

from typing import Protocol

from kink import inject

from .client import SearchClient


@inject
class SearchService():
    def __init__(self, search_client: SearchClient):
        self.search_client = search_client

    def add_serialized_product(self, new: bool, product: dict) -> None:
        index = product["type"]
        if new:
            self.search_client.create(index=index, product=product)
        else:
            self.search_client.update(index=index, product=product)
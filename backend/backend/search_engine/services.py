from typing import List

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

    def get_recommendations(self, sort_list: list, offset: int, index: str) -> list:
        return self.search_client.search(sort=sort_list, offset=offset, index=index)

    def get_autocompletes(self, index: str, field: str, partial: str, brand: str = None) -> List[dict]:
        if field == "brand":
            results = self.search_client.partial_search(field="brand.name", partial=partial, index=index)
            return [{"name": result["brand.name"]} for result in results]
        elif field == "product":
            results = self.search_client.partial_search(field="product.name", partial=partial, index=index, brand=brand)
            return [{"name": result["product.name"]} for result in results]

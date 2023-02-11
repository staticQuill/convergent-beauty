from search_engine.services import SearchService
from search_engine.client import SearchClient
from kink import di

di[SearchClient] = SearchClient()
di[SearchService] = SearchService()

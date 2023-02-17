from unittest.mock import MagicMock

from .views import RecommendationView


def test_sort_param_asc_and_desc_orders(monkeypatch) -> None:
    rec_view = RecommendationView(search_service=MagicMock())

    texture_prefs = {
        "sticky": -2,
        "smooth": 5,
        "cakey": 1.34,
        "slimy": -3.24,
        "wet": 9
    }
    scent_prefs = {
        "fruity": 4,
        "clean": -0.2,
        "sweet": 0,
        "neutral": 15,
        "floral": 2.3
    }

    sort_params = rec_view._generate_sort_params(texture=texture_prefs, scent=scent_prefs)

    assert sort_params == [
        {"neutral": "asc"},
        {"wet": "asc"},
        {"smooth": "asc"},
        {"fruity": "asc"},
        {"slimy": "desc"},
        {"floral": "asc"},
        {"sticky": "desc"},
        {"cakey": "asc"},
        {"clean": "desc"},
        {"sweet": "desc"}
    ]

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
        {"scent_ratings.neutral": {"ignore_unmapped": True, "missing": "_last", "order": "asc", "nested_path": "scent_ratings"}},
        {"texture_ratings.wet": {"ignore_unmapped": True, "missing": "_last", "order": "asc", "nested_path": "texture_ratings"}},
        {"texture_ratings.smooth": {"ignore_unmapped": True, "missing": "_last", "order": "asc", "nested_path": "texture_ratings"}},
        {"scent_ratings.fruity": {"ignore_unmapped": True, "missing": "_last", "order": "asc", "nested_path": "scent_ratings"}},
        {"texture_ratings.slimy": {"ignore_unmapped": True, "missing": "_first", "order": "desc", "nested_path": "texture_ratings"}},
        {"scent_ratings.floral": {"ignore_unmapped" : True, "missing": "_last", "order": "asc", "nested_path": "scent_ratings"}},
        {"texture_ratings.sticky": {"ignore_unmapped" : True, "missing": "_first", "order": "desc", "nested_path": "texture_ratings"}},
        {"texture_ratings.cakey": {"ignore_unmapped" : True, "missing": "_last", "order": "asc", "nested_path": "texture_ratings"}},
        {"scent_ratings.clean": {"ignore_unmapped" : True, "missing": "_first", "order": "desc", "nested_path": "scent_ratings"}},
        {"scent_ratings.sweet": {"ignore_unmapped" : True, "missing": "_first", "order": "desc", "nested_path": "scent_ratings"}},
    ]

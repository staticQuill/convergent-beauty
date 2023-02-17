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
        {"scent_ratings.neutral": {"unmapped_type": "integer","missing": "_last", "order": "asc", "nested_path": "scent_ratings"}},
        {"texture_ratings.wet": {"unmapped_type": "integer","missing": "_last", "order": "asc", "nested_path": "texture_ratings"}},
        {"texture_ratings.smooth": {"unmapped_type": "integer","missing": "_last", "order": "asc", "nested_path": "texture_ratings"}},
        {"scent_ratings.fruity": {"unmapped_type": "integer","missing": "_last", "order": "asc", "nested_path": "scent_ratings"}},
        {"texture_ratings.slimy": {"unmapped_type": "integer","missing": "_first", "order": "desc", "nested_path": "texture_ratings"}},
        {"scent_ratings.floral": {"unmapped_type": "integer","missing": "_last", "order": "asc", "nested_path": "scent_ratings"}},
        {"texture_ratings.sticky": {"unmapped_type": "integer","missing": "_first", "order": "desc", "nested_path": "texture_ratings"}},
        {"texture_ratings.cakey": {"unmapped_type": "integer","missing": "_last", "order": "asc", "nested_path": "texture_ratings"}},
        {"scent_ratings.clean": {"unmapped_type": "integer","missing": "_first", "order": "desc", "nested_path": "scent_ratings"}},
        {"scent_ratings.sweet": {"unmapped_type": "integer","missing": "_first", "order": "desc", "nested_path": "scent_ratings"}},
    ]

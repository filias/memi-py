"""Smoke tests: the game boots, registers its categories, and its data is sane."""

from memi_py import app as app_module
from memi_py.providers import categories as cat


def test_app_builds():
    assert app_module.app is not None


def test_expected_category_keys():
    keys = {p.key for p in cat.PROVIDERS}
    assert keys == {
        "peaks",
        "nature:animals",
        "nature:plants",
        "lakes",
        "valleys",
        "passes",
        "parks",
    }


def test_no_empty_or_duplicate_items():
    for provider in cat.PROVIDERS:
        assert provider.items, f"{type(provider).__name__} has no items"
        assert len(provider.items) == len(set(provider.items)), (
            f"{type(provider).__name__} has duplicate items"
        )


def test_peaks_tags_and_clues():
    peaks = cat.Peaks()
    for item in peaks.items:
        assert peaks.get_tag(item).endswith("m")
        assert peaks.get_clue(item)


def test_scientific_names_cover_all_items():
    for cls in (cat.Animals, cat.Plants):
        for item in cls.items:
            assert item in cls.scientific_names, (
                f"{cls.__name__} missing latin name for {item}"
            )

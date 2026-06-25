import unittest

from eea.geolocation.geodata import parse_geotags_vocabulary
from eea.geolocation.grouping import grouped_geolocation
from eea.geolocation.grouping import serialize_grouped_geolocation


class GroupedGeolocationTest(unittest.TestCase):
    """Test grouped geolocation derivation."""

    def test_parse_geotags_uses_existing_taxonomy_entry_order(self):
        class Vocabulary:
            def iterEntries(self):
                return iter(
                    [
                        ("eea32", "eea32"),
                        ("eea32Cyprus", "eea32Cyprus"),
                        ("eea32Cyprusgeo-146669", "geo-146669"),
                        ("eea32Portugal", "eea32Portugal"),
                        ("eea32Portugalgeo-2264397", "geo-2264397"),
                    ]
                )

        self.assertEqual(
            parse_geotags_vocabulary(Vocabulary()),
            {
                "eea32": {
                    "title": "eea32",
                    "geo-146669": "Cyprus",
                    "geo-2264397": "Portugal",
                }
            },
        )

    def test_returns_largest_group_and_leftovers(self):
        geo_coverage = {
            "geolocation": [
                {"value": "geo-a", "label": "Austria"},
                {"value": "geo-b", "label": "Belgium"},
                {"value": "geo-c", "label": "Croatia"},
                {"value": "geo-extra", "label": "Kyrgyzstan"},
            ]
        }
        geotags = {
            "large": {
                "title": "Large",
                "geo-a": "Austria",
                "geo-b": "Belgium",
                "geo-c": "Croatia",
            },
            "small": {
                "title": "Small",
                "geo-a": "Austria",
                "geo-b": "Belgium",
            },
        }

        self.assertEqual(
            grouped_geolocation(
                geo_coverage,
                geotags=geotags,
                country_mappings={},
            ),
            {
                "groups": [
                    {
                        "value": "large",
                        "label": "Large",
                        "countries": [
                            {"value": "geo-a", "label": "Austria"},
                            {"value": "geo-b", "label": "Belgium"},
                            {"value": "geo-c", "label": "Croatia"},
                        ],
                    }
                ],
                "ungrouped": [{"value": "geo-extra", "label": "Kyrgyzstan"}],
            },
        )

    def test_returns_no_group_for_partial_match(self):
        geo_coverage = {
            "geolocation": [
                {"value": "geo-a", "label": "Austria"},
                {"value": "geo-c", "label": "Croatia"},
            ]
        }
        geotags = {
            "large": {
                "title": "Large",
                "geo-a": "Austria",
                "geo-b": "Belgium",
                "geo-c": "Croatia",
            },
        }

        self.assertEqual(
            grouped_geolocation(
                geo_coverage,
                geotags=geotags,
                country_mappings={},
            ),
            {
                "groups": [],
                "ungrouped": [
                    {"value": "geo-a", "label": "Austria"},
                    {"value": "geo-c", "label": "Croatia"},
                ],
            },
        )

    def test_uses_country_mappings_for_group_country_labels(self):
        geo_coverage = {"geolocation": [{"value": "geo-tr", "label": "Turkiye"}]}
        geotags = {
            "mapped": {
                "title": "Mapped",
                "geo-tr": "Turkey",
            },
        }

        self.assertEqual(
            grouped_geolocation(
                geo_coverage,
                geotags=geotags,
                country_mappings={"Turkey": "Turkiye"},
            ),
            {
                "groups": [
                    {
                        "value": "mapped",
                        "label": "Mapped",
                        "countries": [{"value": "geo-tr", "label": "Turkiye"}],
                    }
                ],
                "ungrouped": [],
            },
        )

    def test_serialize_grouped_geolocation_adds_derived_data(self):
        geo_coverage = {"geolocation": [{"value": "geo-a", "label": "Austria"}]}

        self.assertEqual(
            serialize_grouped_geolocation(
                geo_coverage,
                context=None,
            ),
            {
                "geolocation": [{"value": "geo-a", "label": "Austria"}],
                "grouped_geolocation": {
                    "groups": [],
                    "ungrouped": [{"value": "geo-a", "label": "Austria"}],
                },
            },
        )


def test_suite():
    """Test suite."""
    return unittest.defaultTestLoader.loadTestsFromName(__name__)

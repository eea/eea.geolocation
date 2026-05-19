"""Helpers for derived geographic coverage grouping."""

from eea.geolocation.geodata import get_country_mappings
from eea.geolocation.geodata import get_geotags


def grouped_geolocation(
    geo_coverage,
    context=None,
    geotags=None,
    country_mappings=None,
):
    """Return largest matching geotag group plus ungrouped countries.

    The saved value remains the flat ``geo_coverage["geolocation"]`` list. This
    helper derives an additive public-display structure from taxonomy-backed
    geotags.
    """
    if not isinstance(geo_coverage, dict):
        return {"groups": [], "ungrouped": []}

    selected = geo_coverage.get("geolocation") or []
    selected = [item for item in selected if item.get("value")]
    selected_values = {item["value"] for item in selected}
    selected_labels = {item["value"]: item.get("label") for item in selected}

    if not selected_values:
        return {"groups": [], "ungrouped": []}

    geotags = geotags if geotags is not None else get_geotags(context=context)
    country_mappings = (
        country_mappings
        if country_mappings is not None
        else get_country_mappings(context=context)
    )

    matched_groups = []
    for group_value, group_data in geotags.items():
        countries = []

        for country_value, country_name in group_data.items():
            if country_value == "title":
                continue

            countries.append(
                {
                    "value": country_value,
                    "label": selected_labels.get(country_value)
                    or country_mappings.get(country_name)
                    or country_name,
                }
            )

        if countries and all(
            country["value"] in selected_values for country in countries
        ):
            matched_groups.append(
                {
                    "value": group_value,
                    "label": group_data.get("title") or group_value,
                    "countries": countries,
                }
            )

    matched_groups.sort(key=lambda group: (-len(group["countries"]), group["label"]))
    groups = matched_groups[:1]

    covered_values = {
        country["value"] for group in groups for country in group["countries"]
    }
    ungrouped = [item for item in selected if item["value"] not in covered_values]

    return {"groups": groups, "ungrouped": ungrouped}


def serialize_grouped_geolocation(geo_coverage, context=None):
    """Return geo coverage with additive grouped geolocation data."""
    if not isinstance(geo_coverage, dict):
        return geo_coverage

    value = geo_coverage.copy()
    value["grouped_geolocation"] = grouped_geolocation(value, context=context)
    return value

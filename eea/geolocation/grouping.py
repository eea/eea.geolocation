"""Helpers for derived geographic coverage grouping."""

from collective.taxonomy.interfaces import ITaxonomy
from plone.i18n.normalizer.interfaces import IIDNormalizer
from zope.component import getUtility
from zope.component import queryUtility

GEOTAGS_TAXONOMY = "eea.geolocation.geotags.taxonomy"
COUNTRIES_MAPPING_TAXONOMY = "eea.geolocation.countries_mapping.taxonomy"


def taxonomy_utility_name(name):
    """Return the generated collective.taxonomy utility name."""
    normalizer = queryUtility(IIDNormalizer) or getUtility(IIDNormalizer)
    normalized_name = normalizer.normalize(name).replace("-", "")
    return "collective.taxonomy." + normalized_name


def get_taxonomy_vocabulary(name, context=None, language="en"):
    """Return taxonomy vocabulary for a taxonomy name."""
    try:
        utility_name = taxonomy_utility_name(name)
    except Exception:
        return None

    taxonomy = queryUtility(ITaxonomy, name=utility_name)
    if taxonomy is None:
        return None

    try:
        return taxonomy(context)
    except Exception:
        return taxonomy.makeVocabulary(language)


def get_geotags(context=None, vocabulary=None):
    """Return geotags in the same structure exposed by ``@geodata``."""
    vocabulary = vocabulary or get_taxonomy_vocabulary(
        GEOTAGS_TAXONOMY, context=context
    )
    if vocabulary is None:
        return {}

    geotags = {}
    identifier = "placeholderidentifier"
    data = {}
    country = ""

    for value, _key in vocabulary.iterEntries():
        value = value.encode("latin-1", "ignore").decode("latin-1")

        if identifier not in value:
            identifier = value
            data = {"title": identifier}
            identifier_key = "_".join(value.split(" ")).lower()
            geotags[identifier_key] = data
            continue

        if "geo" not in value:
            country = value.split(identifier)[-1]
            continue

        geotag = value.split(country)[-1]
        data[geotag] = country

    return geotags


def get_country_mappings(context=None):
    """Return country label mappings from taxonomy."""
    vocabulary = get_taxonomy_vocabulary(COUNTRIES_MAPPING_TAXONOMY, context=context)
    if vocabulary is None:
        return {}

    country_mappings = {}
    identifier = "placeholderidentifier"

    for value, _key in vocabulary.iterEntries():
        value = value.encode("latin-1", "ignore").decode("latin-1")

        if identifier not in value:
            identifier = value
            continue

        country = value.split(identifier)[-1] or identifier
        country_mappings[country] = identifier

    return country_mappings


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

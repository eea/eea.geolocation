"""Utilities for taxonomy-backed geolocation data."""

from collective.taxonomy.interfaces import ITaxonomy
from collective.taxonomy import PATH_SEPARATOR
from plone.i18n.normalizer.interfaces import IIDNormalizer
from plone.memoize.ram import cache
from zope.component import getUtility
from zope.component import queryUtility


GEOTAGS_TAXONOMY = "eea.geolocation.geotags.taxonomy"
BIOTAGS_TAXONOMY = "eea.geolocation.biotags.taxonomy"
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


def parse_geotags_vocabulary(vocabulary):
    """Return geotags from a taxonomy vocabulary."""
    geodata = {}
    identifier = "placeholderidentifier"
    data = {}
    country = ""

    for value, _key in vocabulary.iterEntries():
        value = value.replace(PATH_SEPARATOR, "")
        if identifier not in value:
            identifier = value
            data = {"title": identifier}
            identifier_key = "_".join(value.split(" ")).lower()
            geodata[identifier_key] = data

        if "geo" not in value:
            country = value.split(identifier)[-1]
        else:
            geo = value.split(country)[-1]
            data[geo] = country

    return geodata


def parse_biotags_vocabulary(vocabulary):
    """Return biotags from a taxonomy vocabulary."""
    biodata = {}
    identifier = "placeholderidentifier"
    data = {}

    for value, _key in vocabulary.iterEntries():
        value = value.replace(PATH_SEPARATOR, "")
        if identifier not in value:
            identifier = value
            data = {"title": identifier}

        if "latitude" in value:
            data["latitude"] = value.split("latitude")[-1]

        if "longitude" in value:
            data["longitude"] = value.split("longitude")[-1]

        if "Abbreviation" in value:
            identifier_key = value.split("Abbreviation")[-1]
            biodata[identifier_key] = data

    biodata.pop("", None)
    return biodata


def parse_country_mappings_vocabulary(vocabulary):
    """Return country label mappings from a taxonomy vocabulary."""
    countrydata = {}
    identifier = "placeholderidentifier"

    for value, _key in vocabulary.iterEntries():
        value = value.replace(PATH_SEPARATOR, "")
        if identifier not in value:
            identifier = value
        else:
            country = value.split(identifier)[-1] or identifier
            countrydata[country] = identifier

    return countrydata


@cache(lambda method, *args, **kwargs: "geotags")
def get_geotags(context=None):
    """Return geotags in the same structure exposed by ``@geodata``."""
    vocabulary = get_taxonomy_vocabulary(GEOTAGS_TAXONOMY, context=context)
    if vocabulary is None:
        return {}

    return parse_geotags_vocabulary(vocabulary)


@cache(lambda method, *args, **kwargs: "biotags")
def get_biotags(context=None):
    """Return biotags in the same structure exposed by ``@geodata``."""
    vocabulary = get_taxonomy_vocabulary(BIOTAGS_TAXONOMY, context=context)
    if vocabulary is None:
        return {}

    return parse_biotags_vocabulary(vocabulary)


@cache(lambda method, *args, **kwargs: "country_mappings")
def get_country_mappings(context=None):
    """Return country label mappings from taxonomy."""
    vocabulary = get_taxonomy_vocabulary(COUNTRIES_MAPPING_TAXONOMY, context=context)
    if vocabulary is None:
        return {}

    return parse_country_mappings_vocabulary(vocabulary)


def get_geodata(context=None):
    """Return all geolocation taxonomy data exposed by ``@geodata``."""
    return {
        "geotags": get_geotags(context=context),
        "biotags": get_biotags(context=context),
        "country_mappings": get_country_mappings(context=context),
    }

"""Upgrade to 3.0 - Add EEA40 taxonomy group to geotags"""

import logging

from collective.taxonomy import PATH_SEPARATOR
from zope.component import getUtility
from collective.taxonomy.interfaces import ITaxonomy

logger = logging.getLogger("eea.geolocation")

# EEA40 = EEA38 + Ukraine + Moldova (40 member countries)
# Order follows EEA38_2020 with Ukraine and Moldova appended

GROUP_UUID = "ab67bbdf-027d-5a75-8286-ee8409e37e3c"
GROUP_SLUG = "eea40"
GROUP_CAPTION = "EEA40"

COUNTRIES = [
    ("Cyprus", "be8c4bca-368c-5b26-bcaa-f42412551ce4", "4e635e8f-69b8-5565-a92d-d9d33b01270e", "geo-146669"),
    ("Denmark", "7d3b0162-3110-5e7b-b6d8-ce691511d16e", "ad81791a-fe7f-5f53-ab65-7b415ed12f1f", "geo-2623032"),
    ("Norway", "1b5a4381-e9b7-5644-b98a-5af97d4d28c5", "61db8a78-9fc8-5a14-be78-7b9861c3a9f9", "geo-3144096"),
    ("Turkey", "e5ef3220-e7b3-5ff6-92fd-0eb834d4edbf", "b345a934-ec08-57c6-ac93-8d970e9f2dc0", "geo-298795"),
    ("Luxembourg", "cfe99f97-d016-51a7-927d-81367915fdc7", "cadef81b-d4e7-53ab-b849-26af024ab1ac", "geo-2960313"),
    ("Liechtenstein", "74fb7b1a-5613-5b40-a16c-e3b7ebe021d2", "f8745571-f65a-5ee0-a942-b75879ce0046", "geo-3042058"),
    ("Italy", "6a8d9cb2-325b-5620-93ca-79a394aa6f08", "b74eecc3-3e60-5211-b519-a50d0783e7d3", "geo-3175395"),
    ("Sweden", "09940eea-1237-5474-83b1-c7484ae1aade", "8432ab0d-b8bc-5bb1-90ea-35a0d348373f", "geo-2661886"),
    ("Malta", "430e81e0-bbc5-5237-84cd-1a8d74ddb906", "d3525b15-78c8-55de-ab43-531a2869289a", "geo-2562770"),
    ("Montenegro", "3ae74f47-513b-53ae-ae64-6094ef67d8d0", "db3c6b06-bd24-515a-9985-98b77e1611ca", "geo-3194884"),
    ("Slovenia", "28a0cc91-9bbf-528b-923a-21afb1463628", "2b8344b4-cebf-55f4-bfab-f85b042a01fc", "geo-3190538"),
    ("Kosovo", "8375fa5d-f574-559b-8f2e-dcff965ad9ed", "e88f8e01-f9d6-5ef8-884e-4ac8fa3434c9", "geo-831053"),
    ("Greece", "a6eee7aa-acf4-53d4-9de6-1b6107cd99c4", "8501531f-a852-574d-b10a-5035bde63010", "geo-390903"),
    ("Croatia", "76dac824-6200-5ab5-bb3d-213fd5bc6f47", "e38fb3af-b3bf-5f61-9831-7641f9686247", "geo-3202326"),
    ("Netherlands", "c8db0707-c84b-542b-bc51-6b2a6058b18b", "802e8e41-242d-51d2-9927-70c65bef7e92", "geo-2750405"),
    ("Serbia", "a2b497fa-03d0-5189-97cf-d43e3e39bc5f", "d31d959d-82ca-5bb0-b51a-c17174c3cd2a", "geo-6290252"),
    ("Latvia", "83c08fbd-5e82-5aa4-bab0-3619de769e2d", "34907579-ad91-52da-8c22-756cf727aef8", "geo-458258"),
    ("Bosnia and Herzegovina", "0bfbbfdf-85bd-5402-ad16-5ea4d880e2fe", "c495ea12-a472-544e-bc19-4f21755200f8", "geo-3277605"),
    ("Estonia", "a85a61bf-53fa-5b06-b32a-7e1b1324fae5", "b5c1d9cf-f7d2-59b3-a49d-307be278ed5a", "geo-453733"),
    ("Romania", "9dad002c-8094-54dc-a828-5fe476608960", "4ffaafd1-6912-5ff9-a75d-4a28344fa274", "geo-798549"),
    ("Poland", "2d9e5bc7-36eb-50cb-ae4d-270895254ce3", "ee26208d-fd4d-5591-a61c-67cbab9c4c89", "geo-798544"),
    ("Hungary", "a322507f-5e53-5eee-8540-76c26c0112a8", "863405ac-ff52-5c2e-ab0e-96572cc026df", "geo-719819"),
    ("Albania", "f97cf0d4-b5f1-5c8d-af93-b67edb422291", "c099e220-e828-527e-927a-f762f345be5e", "geo-783754"),
    ("Austria", "eb892bab-db91-5b26-8b0a-99b9089bccf6", "760f5340-d54e-5cac-b0de-88399c19f0a5", "geo-2782113"),
    ("France", "3d641de8-65c7-593d-a5b8-9bfa17d541d8", "99ccc016-d141-5e87-9724-522ecbfb4016", "geo-3017382"),
    ("Ireland", "40f8aee8-6cf1-5c42-8ab5-a187fd31cff4", "2a61122b-85c2-516e-8d91-b814f12ee6a8", "geo-2963597"),
    ("Finland", "668788b4-9739-5e56-b223-072d1fc3625d", "b7046e30-41d6-5d4f-a8f4-7b38a54afe51", "geo-660013"),
    ("Bulgaria", "b3e3931a-a2b7-5f69-932f-c6cad984c62f", "b141c8d1-c075-5576-852f-30908c5f60b0", "geo-732800"),
    ("Belgium", "cb99b12d-6152-5e07-a9b1-4e0e5e8b614f", "0de0cf06-4bf8-5046-b0a3-b0053817c3fd", "geo-2802361"),
    ("Germany", "7af0c6bb-80c9-5153-995a-58b4118ca96c", "3ccda0cc-a690-5651-9bd2-510c90745fd3", "geo-2921044"),
    ("Slovakia", "1ba59a04-3f3d-5209-bc55-381972529e96", "d2e72d2e-0ecd-508e-aec2-0773e6b61d50", "geo-3057568"),
    ("Spain", "7b8f4a06-9a8e-52ce-a2ea-64f28d77659d", "f003e1e4-c548-5e99-9493-2ad7193d6fd1", "geo-2510769"),
    ("Lithuania", "7589dd3e-4382-5f20-8025-e528f97a060d", "483c31e2-1ab9-5355-af77-2b5a50d1af1b", "geo-597427"),
    ("North Macedonia", "0cbbfe64-dea7-5d4a-a836-2365a400ed3f", "330bcd07-22ba-561e-bd5e-fe25f148347e", "geo-718075"),
    ("Portugal", "7fe59f07-98c4-55ab-8105-9c80f1fc6922", "14b447f6-fdef-510b-b857-748698d640d6", "geo-2264397"),
    ("Czechia", "bb6d5de4-7f3d-575d-bccb-530f4a47c430", "d71c81d2-76fe-51a1-aef4-8f643d29d694", "geo-3077311"),
    ("Iceland", "2cb67216-8c5b-5d6f-80b6-5db94c346cd3", "9d8d0128-c83a-5e49-9a13-08b9e59ad55e", "geo-2629691"),
    ("Switzerland", "83f7f185-5db2-590c-9847-461baa289b99", "1b9a5c08-6ce8-5cf9-862c-00546692dccb", "geo-2658434"),
    ("Ukraine", "cdd74e5d-9e16-58de-b9a4-ad3e9230f6a7", "4231fd99-310d-53b0-be3d-ca3e398378a9", "geo-690791"),
    ("Moldova", "670de041-60db-55d0-8aca-df3bd9bd7f2d", "47a54e38-574a-5d1a-b47a-b7062283e4f9", "geo-617790"),
]

TAXONOMY_NAME = "collective.taxonomy.eeageolocationgeotagstaxonomy"


def add_eea40_taxonomy(context):
    """Add EEA40 member states group to geotags taxonomy.

    EEA40 = EEA38 + Ukraine + Moldova
    This adds the EEA40 group without touching existing taxonomy data
    or behavior configuration.
    """
    taxonomy = getUtility(ITaxonomy, name=TAXONOMY_NAME)

    if taxonomy is None:
        logger.warning("Taxonomy %s not found, skipping EEA40 import", TAXONOMY_NAME)
        return

    # Build the items list for taxonomy.update()
    # Each item is a (path, identifier) tuple
    # Paths use PATH_SEPARATOR (\u241f) as of taxonomy version 2
    items = []

    # Group level entry
    group_path = PATH_SEPARATOR + GROUP_CAPTION
    group_id = "{}||{}".format(GROUP_UUID, GROUP_SLUG)
    items.append((group_path, group_id))

    # Country and geo-ID entries
    for country_name, country_uuid, geo_uuid, geo_id in COUNTRIES:
        country_path = group_path + PATH_SEPARATOR + country_name
        items.append((country_path, country_uuid))

        geo_path = country_path + PATH_SEPARATOR + geo_id
        items.append((geo_path, geo_uuid))

    taxonomy.update("en", items, clear=False)

    logger.info(
        "Added EEA40 taxonomy group with %d countries to %s",
        len(COUNTRIES),
        TAXONOMY_NAME,
    )
from typing import List
from functools import reduce
from statistics import mean
from hestia_earth.schema import SiteSiteType
from hestia_earth.utils.model import find_term_match
from hestia_earth.utils.lookup import download_lookup, get_table_value, column_name
from hestia_earth.utils.tools import non_empty_list

from .shared import flatten, list_has_props
from .shared import validate_dates, validate_list_dates, validate_list_duplicates, diff_in_years, \
    validate_list_min_max, validate_region, validate_country, validate_coordinates, need_validate_coordinates, \
    validate_area, need_validate_area


SOIL_TEXTURE_IDS = ['sandContent', 'siltContent', 'clayContent']
INLAND_TYPES = [
    SiteSiteType.CROPLAND.value,
    SiteSiteType.PERMANENT_PASTURE.value,
    SiteSiteType.POND.value,
    SiteSiteType.BUILDING.value,
    SiteSiteType.FOREST.value,
    SiteSiteType.OTHER_NATURAL_VEGETATION.value
]


def _measurement_value_average(measurement: dict): return mean(measurement.get('value', [0]))


def _group_measurement_key(measurement: dict):
    keys = non_empty_list([
        str(measurement.get('depthUpper', '')),
        str(measurement.get('depthLower', '')),
        measurement.get('startDate'),
        measurement.get('endDate')
    ])
    return '-'.join(keys) if len(keys) > 0 else 'default'


def _group_measurements_depth(measurements: List[dict]):
    def group_by(group: dict, measurement: dict):
        key = _group_measurement_key(measurement)
        if key not in group:
            group[key] = []
        group[key].extend([measurement])
        return group

    return reduce(group_by, measurements, {})


def _validate_soilTexture_percent(lookup):
    soil_texture_ids = list(lookup.termid)

    def validate_single(measurements: List[dict], measurement: dict, texture_id: str):
        texture = find_term_match(measurements, texture_id, {})
        texture_value = _measurement_value_average(texture)
        term_id = measurement['term']['@id']
        min = get_table_value(lookup, 'termid', term_id, column_name(f"{texture_id}min"))
        max = get_table_value(lookup, 'termid', term_id, column_name(f"{texture_id}max"))
        return min <= texture_value <= max or {
            'level': 'error',
            'dataPath': '.measurements',
            'message': 'is outside the allowed range',
            'params': {
                'term': texture['term'],
                'range': {'min': min, 'max': max}
            }
        }

    def validate_all(measurements: List[dict]):
        values = list(filter(lambda v: v['term']['@id'] in soil_texture_ids, measurements))
        return len(values) == 0 or flatten(map(
            lambda measurement: list(map(lambda id: validate_single(measurements, measurement, id), SOIL_TEXTURE_IDS)),
            values
        ))

    return validate_all


def _validate_soiltTexture_sum(measurements: List[dict]):
    measurements = list(filter(lambda v: v['term']['@id'] in SOIL_TEXTURE_IDS, measurements))
    measurements = list(filter(lambda v: 'value' in v, measurements))
    terms = list(map(lambda v: v['term']['@id'], measurements))
    sum_values = sum(map(lambda v: _measurement_value_average(v), measurements))
    return len(set(terms)) != len(SOIL_TEXTURE_IDS) or 99.5 < sum_values < 100.5 or {
        'level': 'error',
        'dataPath': '.measurements',
        'message': f"sum not equal to 100% for {', '.join(SOIL_TEXTURE_IDS)}"
    }


def validate_soilTexture(measurements: List[dict]):
    soilTexture = download_lookup('soilTexture.csv')
    groupped_measurements = _group_measurements_depth(measurements).values()
    results_sum = list(map(_validate_soiltTexture_sum, groupped_measurements))
    valid_sum = next((x for x in results_sum if x is not True), True)
    results_percent = flatten(map(_validate_soilTexture_percent(soilTexture), groupped_measurements))
    valid_percent = next((x for x in results_percent if x is not True), True)
    return valid_sum if valid_sum is not True else valid_percent


def validate_depths(measurements: List[dict]):
    def validate(values):
        index = values[0]
        measurement = values[1]
        return measurement['depthUpper'] < measurement['depthLower'] or {
            'level': 'error',
            'dataPath': f".measurements[{index}].depthLower",
            'message': 'must be greater than depthUpper'
        }

    results = list(map(validate, enumerate(list_has_props(measurements, ['depthUpper', 'depthLower']))))
    return next((x for x in results if x is not True), True)


def value_range_error(value: int, minimum: int, maximum: int):
    return 'minimum' if minimum is not None and value < minimum else \
        'maximum' if maximum is not None and value > maximum else False


def validate_measurements_value(measurements: List[dict]):
    def validate(values):
        index = values[0]
        measurement = values[1]
        props = measurement.get('term', {}).get('defaultProperties', [])
        mininum = next((prop.get('value') for prop in props if prop.get('term', {}).get('@id') == 'minimum'), None)
        maximum = next((prop.get('value') for prop in props if prop.get('term', {}).get('@id') == 'maximum'), None)
        value = _measurement_value_average(measurement)
        error = value_range_error(value, mininum, maximum) if value is not None else False
        return error is False or ({
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be above {mininum}"
        } if error == 'minimum' else {
            'level': 'error',
            'dataPath': f".measurements[{index}].value",
            'message': f"should be below {maximum}"
        })

    results = list(map(validate, enumerate(measurements)))
    return next((x for x in results if x is not True), True)


def validate_lifespan(infrastructure: List[dict]):
    def validate(values):
        value = values[1]
        index = values[0]
        lifespan = diff_in_years(value.get('startDate'), value.get('endDate'))
        return lifespan == round(value.get('lifespan'), 1) or {
            'level': 'error',
            'dataPath': f".infrastructure[{index}].lifespan",
            'message': f"must equal to endDate - startDate in decimal years (~{lifespan})"
        }

    results = list(map(validate, enumerate(list_has_props(infrastructure, ['lifespan', 'startDate', 'endDate']))))
    return next((x for x in results if x is not True), True)


def validate_site_dates(site: dict):
    return validate_dates(site) or {
        'level': 'error',
        'dataPath': '.endDate',
        'message': 'must be greater than startDate'
    }


def validate_site_coordinates(site: dict):
    return need_validate_coordinates(site) and site.get('siteType') in INLAND_TYPES


def validate_site(site: dict):
    return [
        validate_site_dates(site),
        validate_country(site) if 'country' in site else True,
        validate_region(site) if 'region' in site else True,
        validate_coordinates(site) if validate_site_coordinates(site) else True,
        validate_area(site) if need_validate_area(site) else True
    ] + ([
        validate_list_dates(site, 'measurements'),
        validate_list_min_max(site, 'measurements'),
        validate_soilTexture(site.get('measurements')),
        validate_depths(site.get('measurements')),
        validate_measurements_value(site.get('measurements')),
        validate_list_duplicates(site, 'measurements', [
            'term.@id',
            'method.@id',
            'methodDescription',
            'startDate',
            'endDate',
            'depthUpper',
            'depthLower'
        ])
    ] if 'measurements' in site else []) + ([
        validate_list_dates(site, 'infrastructure'),
        validate_lifespan(site.get('infrastructure'))
    ] if 'infrastructure' in site else [])

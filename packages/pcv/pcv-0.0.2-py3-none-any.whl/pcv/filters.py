import logging
from datetime import datetime
from operator import itemgetter


logger = logging.getLogger(__name__)


def to_iso_date(value):
    """
    handle incomplete iso strings, so we can specify <year> or <year-month>,
    in addition to <year-month-day>
    """
    hyphen_count = value.count('-')
    if hyphen_count < 2:
        value += '-01' * (2 - hyphen_count)
    return value


def as_date(value):
    """
    convert an iso 8601 date string to a datetime.date, return current date
    if string is not a valid iso string (e.g. empty string or "present")
    """
    try:
        return datetime.fromisoformat(to_iso_date(value)).date()
    except ValueError as e:
        logger.debug(e)
        return datetime.today().date()


def reformat(value, format_string='%Y, %b %d'):
    """
    re-format an iso 8601 date string to the specified format, except "present"
    """
    date_string = 'present'
    if value.lower() != date_string:
        date_string = as_date(value).strftime(format_string)
    return date_string


def as_circles(value, max_value=5):
    """
    represent an integer value as black and white circles, on a scale of 0 to
    max_value (we assume integers here...)
    """
    return '●' * value + '○' * (max_value - value)


def sort_and_group(item_list, date_field, group_field, reverse=True):
    """
    sort a list of items by date_field, and "group" successive items with
    identical group_field by removing redundant group_field values
    """
    item_list.sort(key=lambda i: as_date(i[date_field]), reverse=reverse)
    current_group = None
    for item in item_list:
        group = item[group_field].lower()
        if group == current_group:
            del item[group_field]
            logger.debug(f'field deleted: {group}')
        else:
            current_group = group
    return item_list


def sort_and_join_labels(item_list, sort_field='level', reverse=True,
                         delimiter=', '):
    """ sort items by specified field and join item labels """
    sorted_list = sorted(item_list, key=itemgetter(sort_field), reverse=reverse)
    return delimiter.join([item['label'] for item in sorted_list])


def group_by_category(item_list):
    """ collect items by category """
    categories = dict()
    for item in item_list:
        key = item['category']
        if key not in categories:
            categories[key] = []
        categories[key].append(item)
    return categories.items()


def kilo(value):
    return f'{round(value/1000)}k'


def sort_by_level_and_priority(item_list):
    """
    Note that, due to Python's stable sorting, the original order is
    preserved if items have the same value.
    """
    item_list.sort(key=itemgetter('level'), reverse=True)
    item_list.sort(key=itemgetter('priority'), reverse=False)
    return item_list


def minimum_level_and_priority(item_list, level=0, priority=float('inf'),
                               exclude=None):
    """
    create a new list with items that have sufficient level and priority
    """
    if exclude is None:
        exclude = []
    return [item for item in item_list
            if (item['priority'] <= priority and
                ('level' not in item or item['level'] >= level) and
                item.get('label', '').lower() not in exclude)
            ]

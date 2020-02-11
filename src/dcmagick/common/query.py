def _or(obj, value):
    result = False
    for query in value:
        result |= _match(obj, query)
    return result


def _and(obj, value):
    result = True
    for query in value:
        result &= _match(obj, query)
    return result


def _eq(obj, value):
    return obj == value


def _ne(obj, value):
    return not _eq(obj, value)


def _in(obj, value):
    return obj in value


def _gt(obj, value):
    return value < obj


def _gte(obj, value):
    return _gt(obj, value) or _eq(obj, value)


def _lt(obj, value):
    return not _gte(obj, value)


def _lte(obj, value):
    return not _gt(obj, value)


def _get_op(key):
    def _eq_with_key(obj, value):
        obj_attr = getattr(obj, key) if hasattr(obj, key) else obj[key]
        return _eq(obj_attr, value)

    return {
        "$eq": _eq,
        "$ne": _ne,
        "$in": _in,
        "$gt": _gt,
        "$gte": _gte,
        "$lt": _lt,
        "$lte": _lte,
    }.get(key, _eq_with_key)


def _match(obj, query):
    """
    >>> _match({}, {})
    True
    >>> _match({'a': 100}, {'a': 100})
    True
    >>> _match({'a': 100}, {'a': 200})
    False
    >>> _match({'a': {'b': {'c': 'd'}}}, {'a': {'b' : {'c': 'd'}}})
    True
    >>> _match({'a': 'b'}, {'a': {'$in' : ['c', 'd']}})
    False
    >>> _match({'a': 'b'}, {'a': {'$in' : ['c', 'b']}})
    True
    >>> _match({'a': 100}, {'a': {'$gt' : 50, '$lt': 200}})
    True
    >>> _match({'a': 100}, {'a': {'$gt' : 50, '$lte': 100}})
    True
    >>> _match({'a': 100}, {'a': {'$ne' : 50}})
    True
    """
    result = True
    for key, value in query.items():
        if isinstance(value, dict):
            ret = _match(obj[key], value)
        else:
            ret = _get_op(key)(obj, value)
        result &= ret
    return result


def match(query, slice_proxy):
    try:
        result = _match(slice_proxy, query)
    except Exception:
        return False
    return result

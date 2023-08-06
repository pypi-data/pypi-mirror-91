#!/usr/bin/env python
# file: json.py
# auth: walker

"""
客制化JSON 輸出
"""

import json
from json import loads
from json.decoder import JSONDecoder, JSONDecodeError

# 其它類型解析
def default(val):
    from datetime import datetime
    if isinstance(val, datetime):
        return val.strftime('%Y-%m-%d %H:%M:%S')
    raise TypeError(f'Object of type {val.__class__.__name__} '
                                    f'is not JSON serializable')
# 調整默認值
def dumps(obj, *, skipkeys=False, ensure_ascii=False, check_circular=True,
        allow_nan=True, cls=None, indent=None, separators=None,
        default=default, sort_keys=False, **kw):

    # cached encoder
    if (not skipkeys and ensure_ascii and
        check_circular and allow_nan and
        cls is None and indent is None and separators is None and
        default is None and not sort_keys and not kw):
        return _default_encoder.encode(obj)
    if cls is None:
        cls = json.JSONEncoder
    return cls(
        skipkeys=skipkeys, ensure_ascii=ensure_ascii,
        check_circular=check_circular, allow_nan=allow_nan, indent=indent,
        separators=separators, default=default, sort_keys=sort_keys,
        **kw).encode(obj)

json.dumps = dumps

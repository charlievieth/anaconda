
# Copyright (C) 2013 - Oscar Campos <oscar.campos@member.fsf.org>
# This program is Free Software see LICENSE file for details

"""Anaconda JsonServer contexts
"""

import json
from contextlib import contextmanager


@contextmanager
def json_decode(data):
    yield json.loads(data.decode('ascii'))


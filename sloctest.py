#!/usr/bin/env python

import logging.config

logging.config.fileConfig('logging.ini')

from code_scientist.instruments import sloc
from code_scientist.code import file_object

s = sloc.SLOCCounter()
f = file_object.File(name='tests/code/test_file_object.py',
        file_type='python')

s.execute(f)

print f.properties['SLOC']

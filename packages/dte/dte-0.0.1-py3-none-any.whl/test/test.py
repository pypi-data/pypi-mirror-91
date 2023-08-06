#!/usr/bin/env -S python -m pytest 
from io import StringIO
from subprocess import Popen, PIPE
import code
import os
from os import path as op
import re
import sys
import unittest

pathname = op.dirname(sys.argv[0])
print('full path =', op.abspath(pathname))

days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
days_abbrev = [d[:3] for d in days]

test_expectancy = {
        '(T-1d).dow' : lambda r: r in days,
        'T-10d'      : lambda r: len(r) == 26,
        'T-1.5d'     : lambda r: len(r) == 26,
        'T.day'      : lambda r: re.match(r'\d+', r),
        'YD.day'     : lambda r: re.match(r'\d+', r),
        'T.dow'      : lambda r: r in days,
        'wait(1s)'   : lambda r: True,
        # 'seconds since '      : lambda r: r in days,
        }

class Capturing(list):
    def __enter__(self):
        self._stdout = sys.stdout
        sys.stdout = self._stringio = StringIO()
        return self
    def __exit__(self, *args):
        self.extend(self._stringio.getvalue().splitlines())
        del self._stringio    # free up some memory
        sys.stdout = self._stdout

def parse(test):
    with Capturing() as output:
        yacc.parse(test)
    return output

class Tester(unittest.TestCase):

    def test_stuff(self):
        test_outputs = []
        dte_location = os.path.dirname(os.path.realpath(__file__)) \
                                 + op.sep + '..'   \
                                 + op.sep + 'dte' \
                                 + op.sep + 'dte'
        for test,expectancy in test_expectancy.items():
            p = Popen(dte_location, stdin=PIPE, stdout=PIPE)
            out,err = p.communicate(test.encode('utf-8'))
            out = out.decode('utf-8').replace('\n','')
            assert expectancy(out) and not err

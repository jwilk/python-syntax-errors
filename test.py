#!/usr/bin/env python
# encoding=UTF-8

# Copyright © 2017-2022 Jakub Wilk <jwilk@jwilk.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the “Software”), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import glob
import re
import sys
import unittest

pyver = sys.version_info

def t(ver):
    path = 'since-%s.py' % ver
    ver = tuple(map(int, ver.split('.')))
    file = open(path, 'r')
    try:
        code = file.read()
    finally:
        file.close()
    try:
        code = compile(code, path, 'exec')
        exec(code, {}, {})
    except SyntaxError:
        if pyver >= ver:
            raise AssertionError('%s is not syntactically valid with Python %d.%d' % (path, pyver[0], pyver[1]))
        _, exc, _ = sys.exc_info()
        msg = '# Python >= %d.%d is required' % ver
        msg = msg.replace(' >= 3.0 ', ' 3 ')
        msg_re = re.compile(re.escape(msg) + '\\b')
        if not msg_re.search(exc.text):
            raise AssertionError('%s version requirement message is missing with Python %d.%d' % (path, pyver[0], pyver[1]))
    else:
        if pyver < ver:
            raise AssertionError('%s is syntactically valid with Python %d.%d' % (path, pyver[0], pyver[1]))

class Test(unittest.TestCase):

    def _test(self, version):
        t(version)

    def __str__(self):
        version = unittest.TestCase.__str__(self).split('|')[1]
        return 'Python ' + version

def add_tests():
    versions = []
    for path in glob.glob('since-*.py'):
        match = re.match('^since-([0-9.]+)[.]py$', path)
        ver = match.group(1)
        key = tuple(map(int, ver.split('.')))
        versions += [(key, ver)]
    versions.sort()
    for i, (_, ver) in enumerate(versions):
        def method(self, ver=ver):
            t(ver)
        setattr(Test, 'test_%02d|%s|' % (i, ver), method)

add_tests()

if __name__ == '__main__':
    unittest.main()

# vim:ts=4 sts=4 sw=4 et

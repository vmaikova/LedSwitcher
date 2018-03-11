#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `ledswitcher` package."""

import sys
sys.path.append('.')
import pytest
from ledswitcher import taskResult


@pytest.fixture
def test_url():
    result = taskResult("http://claritytrec.ucd.ie/~alawlor/comp30670/input_assign3.txt")
    assert result == 400410

def test_file():
    result = taskResult("../tests/testfiles/test.txt")
    assert result == 3

def main():
    test_url()
    test_file()

if __name__ == '__main__':
    test_url()
    test_file()

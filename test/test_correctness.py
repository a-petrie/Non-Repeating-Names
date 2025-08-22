import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '*')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'common')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'naive')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'prefilter')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'linear_time')))

import unittest

from utils import load_dataset

import naive
import prefilter
import linear_time

class TestNonRepeatingNames(unittest.TestCase):

    def setUp(self):
        self.first_names, self.last_names = load_dataset()
        self.first_names = self.first_names[:750]
        self.last_names = self.last_names[-1000:]

        with open("result.txt") as f:
            self.expected = sorted([name.strip() for name in f.readlines()])

    def test_naive(self):
        actual = sorted(list(naive.non_repeating(self.first_names, self.last_names)))
        self.assertEqual(len(actual), len(self.expected))
        self.assertListEqual(actual, self.expected)

    def test_prefilter(self):
        actual = sorted(list(prefilter.non_repeating(self.first_names, self.last_names)))
        self.assertListEqual(actual, self.expected)

    def test_linear_time(self):
        actual = sorted(list(linear_time.non_repeating(self.first_names, self.last_names)))
        self.assertListEqual(actual, self.expected)

    def test_should_be_robust_against_missing_characters(self):
        first_names = ["jim"]
        last_names = ["bean"]
        expected = ["jim bean"]

        actual = list(linear_time.non_repeating(first_names, last_names))
        self.assertListEqual(actual, expected)

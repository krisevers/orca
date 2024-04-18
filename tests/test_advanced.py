# -*- coding: utf-8 -*-

from .context import orca

import unittest


class AdvancedTestSuite(unittest.TestCase):
    """Advanced test cases."""

    def test_thoughts(self):
        self.assertIsNone(orca.Orca)


if __name__ == '__main__':
    unittest.main()

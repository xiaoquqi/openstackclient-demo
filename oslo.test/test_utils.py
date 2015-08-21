#!/usr/bin/env python

from testtools import TestCase
from myproject import silly

from oslotest import base

class TestSillySquare(TestCase):
    """Tests for silly square function."""

    def test_square(self):
        # 'square' takes a number and multiplies it by itself.
        result = silly.square(7)
        self.assertEqual(result, 49)

    def test_square_bad_input(self):
        # 'square' raises a TypeError if it's given bad input, say a
        # string.
        self.assertRaises(TypeError, silly.square, "orange")


class TestSillySquareOslo(base.BaseTestCase):

    def setUp(self):
        super(TestSillySquareOslo, self).setUp()

    def test_square(self):
        # 'square' takes a number and multiplies it by itself.
        result = silly.square(7)
        self.assertEqual(result, 49)

    def test_square_bad_input(self):
        # 'square' raises a TypeError if it's given bad input, say a
        # string.
        self.assertRaises(TypeError, silly.square, "orange")

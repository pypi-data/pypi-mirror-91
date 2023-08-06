import unittest

from fitpy import Body


class Test_Body(unittest.TestCase):
    def test_init(self):
        b1 = Body(
            30,
            180,
            80,
            'female',
        )

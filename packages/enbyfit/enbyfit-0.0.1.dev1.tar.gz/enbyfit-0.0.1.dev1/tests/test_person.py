import unittest

from fitpy import Person

class Test_Person(unittest.TestCase):
    def test_init(self):
        ''' See if Name is capitalized '''
        p1 = Person('alice')
        assert p1._name == 'Alice'


if '__main__' == __name__:
    unittest.main()

import unittest
from add_numbers import adding

class TestAddNumbers(unittest.TestCase):
    def test_add_numbers(self):
        # Test adding two positive numbers
        self.assertEqual(adding(2, 3), 5)
        # Test adding positive and negative numbers
        self.assertEqual(adding(-1, 5), 4)
        # Test adding two negative numbers
        self.assertEqual(adding(-3, -2), -5)
        # Test adding zero
        self.assertEqual(adding(0, 0), 0)
        self.assertEqual(adding(0, 5), 5)

if __name__ == '__main__':
    unittest.main()

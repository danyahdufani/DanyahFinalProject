import unittest

class TestAddNumbers(unittest.TestCase):
    def test_add_numbers(self):
        # Test adding two positive numbers
        self.assertEqual(add_numbers(2, 3), 5)
        # Test adding positive and negative numbers
        self.assertEqual(add_numbers(-1, 5), 4)
        # Test adding two negative numbers
        self.assertEqual(add_numbers(-3, -2), -5)
        # Test adding zero
        self.assertEqual(add_numbers(0, 0), 0)
        self.assertEqual(add_numbers(0, 5), 5)

if __name__ == '__main__':
    unittest.main()

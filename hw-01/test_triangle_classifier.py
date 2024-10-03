import unittest
from triangle_classifier import classify_triangle

class TestClassifyTriangle(unittest.TestCase):

    def test_equilateral(self):
        self.assertEqual(classify_triangle(5, 5, 5), "Equilateral ")

    def test_isosceles(self):
        self.assertEqual(classify_triangle(5, 5, 8), "Isosceles ")

    def test_scalene(self):
        self.assertEqual(classify_triangle(3, 4, 5), "Scalene Right")

    def test_right_triangle(self):
        self.assertEqual(classify_triangle(6, 8, 10), "Scalene Right")

    def test_not_a_triangle(self):
        self.assertEqual(classify_triangle(1, 2, 3), "Not a triangle")

    # Test for bad input handling
    def test_invalid_input_non_numeric(self):
        self.assertEqual(classify_triangle("a", 4, 5), "Invalid input")

    def test_invalid_input_negative(self):
        self.assertEqual(classify_triangle(-1, 2, 3), "Invalid input")

    def test_invalid_input_zero(self):
        self.assertEqual(classify_triangle(0, 2, 3), "Invalid input")

if __name__ == "__main__":
    unittest.main()

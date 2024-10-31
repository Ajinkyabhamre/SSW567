# -*- coding: utf-8 -*-
"""
Module for classifying triangles based on side lengths.

Functions:
    classify_triangle(a, b, c): Classifies a triangle based on side lengths.
"""

def classify_triangle(a, b, c):
    """
    This function returns a string with the type of triangle from three integer values
    corresponding to the lengths of the three sides of the triangle.

    Args:
        a (int): Length of side a.
        b (int): Length of side b.
        c (int): Length of side c.

    Returns:
        str: Type of triangle: 'Equilateral', 'Isosceles', 'Scalene', 'Right', or 'NotATriangle'.
        Returns 'InvalidInput' if inputs are invalid.
    """
    # Verify inputs are integers and within the valid range
    if not all(isinstance(x, int) and 0 < x <= 200 for x in (a, b, c)):
        return 'InvalidInput'

    # Check if it's a valid triangle
    if (a >= b + c) or (b >= a + c) or (c >= a + b):
        return 'NotATriangle'

    # Check for right triangle
    sides = sorted([a, b, c])
    if (sides[0] ** 2 + sides[1] ** 2) == (sides[2] ** 2):
        return 'Right'
    # Determine triangle type
    if a == b == c:
        return 'Equilateral'
    if a == b or b == c or a == c:
        return 'Isosceles'
    return 'Scalene'

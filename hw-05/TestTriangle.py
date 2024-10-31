# -*- coding: utf-8 -*-
"""
Updated Jan 21, 2018
The primary goal of this file is to demonstrate a simple unittest implementation
@author: jrr
@author: rk
"""
import unittest
from triangle import classify_triangle
# This code implements the unit test functionality
# https://docs.python.org/3/library/unittest.html has a nice description of the framework

class TestTriangles(unittest.TestCase):
# define multiple sets of tests as functions with names that begin

    def testRightTriangleA(self):
        self.assertEqual(classify_triangle(3,4,5),'Right','3,4,5 is a Right triangle')
        
    def testRightTriangleB(self):
        self.assertEqual(classify_triangle(5,3,4),'Right','5,3,4 is a Right triangle')
        
    def testEquilateralTriangles(self):
        self.assertEqual(classify_triangle(1,1,1),'Equilateral','1,1,1 should be equilateral')
        
    # Additional test cases for invalid inputs
    def testInvalidInputsA(self):
        self.assertEqual(classify_triangle(201,150,150),'InvalidInput')
        self.assertEqual(classify_triangle(-1,2,3),'InvalidInput')
        self.assertEqual(classify_triangle(1.1,2,3),'InvalidInput')
        
    # Test cases for not a triangle
    def testNotATriangle(self):
        self.assertEqual(classify_triangle(1,1,3),'NotATriangle')
        self.assertEqual(classify_triangle(2,4,2),'NotATriangle')
        
    # Test cases for isosceles triangle
    def testIsoscelesTriangle(self):
        self.assertEqual(classify_triangle(2,2,3),'Isosceles')
        self.assertEqual(classify_triangle(3,4,3),'Isosceles')
        
    # Test cases for scalene triangle
    def testScaleneTriangle(self):
        self.assertEqual(classify_triangle(3,4,6),'Scalene')
        self.assertEqual(classify_triangle(5,7,9),'Scalene')
        
    # Additional right triangle test cases
    def testRightTriangleC(self):
        self.assertEqual(classify_triangle(6,8,10),'Right')
        self.assertEqual(classify_triangle(8,15,17),'Right')
        
    # Boundary value test cases
    def testBoundaryValues(self):
        self.assertEqual(classify_triangle(200,200,200),'Equilateral')
        self.assertEqual(classify_triangle(1,1,1),'Equilateral')
        
    # Edge cases
    def testEdgeCases(self):
        self.assertEqual(classify_triangle(0,1,2),'InvalidInput')
        self.assertEqual(classify_triangle(1,1,2),'NotATriangle')



if __name__ == '__main__':
    print('Running unit tests')
    unittest.main()

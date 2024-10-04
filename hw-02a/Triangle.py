def classifyTriangle(a,b,c):
    """
    This function returns a string with the type of triangle from three integer values
    corresponding to the lengths of the three sides of the Triangle.
    
    return:
        If all three sides are equal, return 'Equilateral'
        If exactly one pair of sides are equal, return 'Isosceles'
        If no pair of sides are equal, return 'Scalene'
        If not a valid triangle, then return 'NotATriangle'
        If the sum of squares of two sides equals the square of the third side, then return 'Right'
    """
    # Verify that all inputs are integers
    if not(isinstance(a,int) and isinstance(b,int) and isinstance(c,int)):
        return 'InvalidInput'
        
    # Require that the input values be >= 0 and <= 200
    if a > 200 or b > 200 or c > 200:
        return 'InvalidInput'
    if a <= 0 or b <= 0 or c <= 0:
        return 'InvalidInput'
    
    # Check if it's a valid triangle
    # The sum of any two sides must be greater than the third side
    if (a >= (b + c)) or (b >= (a + c)) or (c >= (a + b)):
        return 'NotATriangle'
        
    # Now we know that we have a valid triangle
    # Check if it's a right triangle
    # Use sorted to order sides from smallest to largest
    sides = sorted([a, b, c])
    if (sides[0] * sides[0] + sides[1] * sides[1]) == (sides[2] * sides[2]):
        return 'Right'
    
    # Check for equilateral triangle
    if a == b and b == c:
        return 'Equilateral'
    
    # Check for isosceles triangle
    elif a == b or b == c or a == c:
        return 'Isosceles'
    
    # If we get here, it must be scalene
    else:
        return 'Scalene'
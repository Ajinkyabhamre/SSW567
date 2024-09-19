def classify_triangle(a, b, c):
    # Handle invalid input 
    if not all(isinstance(side, (int, float)) and side > 0 for side in [a, b, c]):
        return "Invalid input"

    # Check if the sides form a valid triangle
    if a + b <= c or a + c <= b or b + c <= a:
        return "Not a triangle"

    # Check for right triangle
    if a**2 + b**2 == c**2 or a**2 + c**2 == b**2 or b**2 + c**2 == a**2:
        right_triangle = "Right"
    else:
        right_triangle = ""

    # Check for equilateral triangle
    if a == b == c:
        return "Equilateral " + right_triangle

    # Check for isosceles triangle
    if a == b or a == c or b == c:
        return "Isosceles " + right_triangle

    # If none of the above, it's scalene
    return "Scalene " + right_triangle

if __name__ == "__main__":
    sides = [(3, 4, 5), (2, 2, 2), (3, 3, 5), (1, 1, 3), ("a", 2, 2), (-1, 2, 3)]
    for a, b, c in sides:
        result = classify_triangle(a, b, c)
        print(f"Triangle with sides {a}, {b}, {c} is {result}")

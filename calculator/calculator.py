def calculate(a, b, operation):
    if operation == '+':
        result = a + b
    elif operation == '-':
        result = a - b
    elif operation == '*':
        result = a * b
    elif operation == '/':
        result = a / b
    else:
        result = "Invalid operation"
    print(f"Result: {result}")

# Example usage
calculate(5, 3, '+')
calculate(10, 4, '-')
calculate(6, 2, '*')
calculate(8, 2, '/')
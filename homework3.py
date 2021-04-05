def fibonacci(n):
    a, b = 1, 1
    for i in range(n):
        yield a
        a, b = b, a + b

data = list(fibonacci(10))
print(data)

[1, 1, 2, 3, 5, 8, 13, 21, 34, 55]

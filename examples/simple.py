def foo(x):
    x = x ** 5
    return bar(x)

def bar(y):
    y = y / 12
    return y

print foo(100)

# Python Decorators

## Introduction
Decorators are a powerful and useful tool in Python that allow you to modify the behavior of a function or class. They are often used to add functionality to existing code in a clean and readable way.

## How Decorators Work
A decorator is a function that takes another function as an argument and returns a new function that usually extends the behavior of the original function. Decorators are applied using the `@decorator_name` syntax above the function definition.

## Example
```python
def my_decorator(func):
    def wrapper():
        print("Something is happening before the function is called.")
        func()  
        print("Something is happening after the function is called.")
    return wrapper

@my_decorator
def say_hello():
    print("Hello!")
    
say_hello()
```

In this example, `my_decorator` is a decorator that adds behavior before and after the `say_hello` function is called.

## Common Use Cases
- **Logging**: Track events that happen when some code runs.
- **Authorization**: Check if a user has permission to perform an action.
- **Caching**: Store the results of expensive function calls and reuse them when the same inputs occur again.
- **Validation**: Ensure that the inputs to a function are valid.

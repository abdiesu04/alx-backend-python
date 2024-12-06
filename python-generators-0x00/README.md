# Python Generators

This project focuses on understanding and implementing Python generators. Generators are a simple way of creating iterators using a function that yields values one at a time, allowing for efficient memory usage and lazy evaluation.

## What I Did

- Learned the concept of generators in Python.
- Implemented various generator functions.
- Explored the use of `yield` keyword.
- Practiced creating and using generator expressions.

## Key Concepts

- **Generators**: Functions that return an iterable set of items, one at a time, in a special way.
- **Yield**: A keyword used in generator functions to return a value and pause the function’s execution, which can be resumed later.

## Usage

To use a generator function, simply call it like a normal function. Instead of returning a single value, it returns a generator object that can be iterated over.

```python
def my_generator():
    yield 1
    yield 2
    yield 3

gen = my_generator()
for value in gen:
    print(value)
```

This will output:
```
1
2
3
```

## Benefits of Generators

- **Memory Efficiency**: Generators do not store the entire sequence in memory.
- **Lazy Evaluation**: Values are produced only when needed, which can improve performance.

## Conclusion

Generators are a powerful feature in Python that can help write more efficient and readable code. This project provided hands-on experience with creating and using generators effectively.

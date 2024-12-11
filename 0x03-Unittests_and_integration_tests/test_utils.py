#!/usr/bin/env python3
import unittest
from parameterized import parameterized

def access_nested_map(nested_map, path):
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(f"Key {key} not found in the nested map.")
        current = current[key]
    return current

class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

if __name__ == "__main__":
    unittest.main()

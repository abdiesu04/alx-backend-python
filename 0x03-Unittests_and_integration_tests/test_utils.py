#!/usr/bin/env python3
import unittest
from parameterized import parameterized

def access_nested_map(nested_map, path):
    
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(f"Key '{key}' not found.")
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

    # @parameterized.expand([
    #     ({}, ("a",), "Key 'a' not found."),
    #     ({"a": 1}, ("a", "b"), "Key 'b' not found."),
    # ])
    # def test_access_nested_map_raises(self, nested_map, path, expected_message):
    #     with self.assertRaises(KeyError) as context:
    #         access_nested_map(nested_map, path)
    #     print()
    #     self.assertEqual(str(context.exception), expected_message)

if __name__ == "__main__":
    unittest.main()




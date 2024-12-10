from parameterized import parameterized
import unittest


def access_nested_map(nested_map, path):
    """
    Safely access a value in a nested dictionary using a list or tuple of keys.
    """
    current = nested_map
    for key in path:
        if key not in current:
            raise KeyError(f"Key {key} not found in the nested map.")
        current = current[key]
    return current


class TestAccessNestedMap(unittest.TestCase):
    @parameterized.expand([
        # Test cases: (description, nested_map, path, expected)
        ("single_key", {"a": 1}, ("a",), 1),
        ("nested_key", {"a": {"b": 2}}, ("a",), {"b": 2}),
        ("nested_deep_key", {"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map_valid(self, name, nested_map, path, expected):
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        # Test cases for KeyError: (description, nested_map, path)
        ("missing_nested_key", {"a": {"b": 2}}, ("a", "c")),
        ("missing_top_key", {"a": 1}, ("b",)),
    ])
    def test_access_nested_map_invalid(self, name, nested_map, path):
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


if __name__ == "__main__":
    unittest.main()

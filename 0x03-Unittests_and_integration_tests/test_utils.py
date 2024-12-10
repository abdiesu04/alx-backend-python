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
    def test_access_nested_map(self):
        # Test case 1
        nested_map = {"a": 1}
        path = ("a",)
        self.assertEqual(access_nested_map(nested_map, path), 1)

        # Test case 2
        nested_map = {"a": {"b": 2}}
        path = ("a",)
        self.assertEqual(access_nested_map(nested_map, path), {"b": 2})

        # Test case 3
        nested_map = {"a": {"b": 2}}
        path = ("a", "b")
        self.assertEqual(access_nested_map(nested_map, path), 2)

        # Test case 4: Missing key
        nested_map = {"a": {"b": 2}}
        path = ("a", "c")
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


if __name__ == "__main__":
    unittest.main()

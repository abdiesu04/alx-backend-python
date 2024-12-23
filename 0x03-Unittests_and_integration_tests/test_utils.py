#!/usr/bin/env python3
"""
Module for testing utilities with unittest.

This module contains test cases for the following:
- Accessing nested maps (`access_nested_map`)
- Fetching JSON data (`get_json`)
- Memoization (`memoize`)
"""

import unittest
from parameterized import parameterized
from unittest.mock import patch, Mock
from utils import get_json
from utils import access_nested_map
from utils import memoize


class TestAccessNestedMap(unittest.TestCase):
    """
    Test suite for the `access_nested_map` utility.
    """

    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected):
        """
        Test `access_nested_map` for valid keys.
        """
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",)),
        ({"a": 1}, ("a", "b")),
    ])
    def test_access_nested_map_exception(self, nested_map, path):
        """
        Test `access_nested_map` raises KeyError for invalid keys.
        """
        with self.assertRaises(KeyError):
            access_nested_map(nested_map, path)


class TestGetJson(unittest.TestCase):
    """
    Test suite for the `get_json` utility.
    """

    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    def test_get_json(self, test_url, test_payload):
        """
        Test `get_json` for fetching data from a URL.
        """
        with patch('utils.requests.get') as mock_get:
            mock_response = Mock()
            mock_response.json.return_value = test_payload
            mock_get.return_value = mock_response

            result = get_json(test_url)
            self.assertEqual(result, test_payload)
            mock_get.assert_called_once_with(test_url)


class TestMemoize(unittest.TestCase):
    """
    Test suite for the `memoize` utility.
    """

    class TestClass:
        """
        A test class to demonstrate the `memoize` decorator.
        """

        def a_method(self):
            """
            A simple method that returns a fixed value.
            """
            return 42

        @memoize
        def a_property(self):
            """
            A memoized property that calls `a_method` once.
            """
            return self.a_method()

    def test_memoize(self):
        """
        Test `memoize` to ensure it caches results correctly.
        """
        with patch.object(self.TestClass, 'a_method', return_value=42) as mock_method:  # noqa: E501
            obj = self.TestClass()
            result1 = obj.a_property
            result2 = obj.a_property

            self.assertEqual(result1, 42)
            self.assertEqual(result2, 42)
            mock_method.assert_called_once()


if __name__ == "__main__":
    unittest.main()

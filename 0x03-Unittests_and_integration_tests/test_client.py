#!/usr/bin/env python3
import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch("client.get_json") 
    def test_org(self, org_name, expected_output, mock_get_json):
        # Set the mock's return value
        mock_get_json.return_value = expected_output

        # Create a client and test the method
        client = GithubOrgClient(org_name)
        result = client.org

        # Validate the output
        self.assertEqual(result, expected_output)

        # Ensure the mocked function was called with the correct URL
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")


if __name__ == "__main__":
    unittest.main()

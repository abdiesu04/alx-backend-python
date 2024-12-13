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

    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google/repos"),
        ("abc", "https://api.github.com/orgs/abc/repos")
    ])
    @patch("client.GithubOrgClient.org")
    def test_public_repos_url(self, org_name, expected_url, mock_org):
        # Mocked payload for the org property
        mock_org.return_value = {"repos_url": expected_url}

        # Create a client and test the _public_repos_url property
        client = GithubOrgClient(org_name)
        result = client._public_repos_url

        # Validate the output
        self.assertEqual(result, expected_url)


if __name__ == "__main__":
    unittest.main()

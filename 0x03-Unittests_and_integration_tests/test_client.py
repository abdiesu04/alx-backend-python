#!/usr/bin/env python3
"""
This module contains unittests for the GithubOrgClient class.
"""

import unittest
from unittest.mock import patch
from parameterized import parameterized
from client import GithubOrgClient
import utils


class TestGithubOrgClient(unittest.TestCase):
    """
    Test suite for the GithubOrgClient class.
    """

    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch("client.get_json")
    def test_org(self, org_name, expected_output, mock_get_json):
        """
        Test the `GithubOrgClient.org` method.

        Args:
            org_name (str): The name of the organization to test.
            expected_output (dict): Expected output from `get_json`.
            mock_get_json (Mock): Mocked `get_json` function.

        Validates:
            - `org` method returns the expected output.
            - `get_json` is called once with the correct URL.
        """
        mock_get_json.return_value = expected_output
        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected_output)
        mock_get_json.assert_called_once_with(
            f"https://api.github.com/orgs/{org_name}"
        )

    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google/repos"),
        ("abc", "https://api.github.com/orgs/abc/repos")
    ])
    @patch("client.GithubOrgClient.org",
           new_callable=unittest.mock.PropertyMock)
    def test_public_repos_url(self, org_name, expected_url, mock_org):
        """
        Test the `_public_repos_url` property.

        Args:
            org_name (str): Name of the organization.
            expected_url (str): Expected `repos_url`.
            mock_org (Mock): Mocked `org` property.

        Validates:
            - `_public_repos_url` returns the expected URL.
        """
        mock_org.return_value = {"repos_url": expected_url}
        client = GithubOrgClient(org_name)
        result = client._public_repos_url
        self.assertEqual(result, expected_url)

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url",
           new_callable=unittest.mock.PropertyMock)
    def test_public_repos(self, mock_public_repos_url, mock_get_json):
        """
        Test the `public_repos` method.

        Args:
            mock_public_repos_url (Mock): Mocked `_public_repos_url` property.
            mock_get_json (Mock): Mocked `get_json` function.

        Validates:
            - `public_repos` returns a list of repository names.
            - `_public_repos_url` is accessed once.
            - `get_json` is called with the correct URL.
        """
        mock_get_json.return_value = [
            {"name": "repo1"},
            {"name": "repo2"}
        ]
        mock_public_repos_url.return_value = (
            "https://api.github.com/orgs/test_org/repos"
        )
        client = GithubOrgClient("test_org")
        result = client.public_repos()
        self.assertEqual(result, ["repo1", "repo2"])
        mock_public_repos_url.assert_called_once()
        mock_get_json.assert_called_once_with(
            "https://api.github.com/orgs/test_org/repos"
        )

    @parameterized.expand([
        ({"license": {"key": "my_license"}}, "my_license", True),
        ({"license": {"key": "other_license"}}, "my_license", False)
    ])
    @patch("utils.access_nested_map")
    def test_has_license(self, repo, license_key, expected,
                         mock_access_nested_map):
        """
        Test the `has_license` method.

        Args:
            repo (dict): Repository information.
            license_key (str): License key to check.
            expected (bool): Expected result.
            mock_access_nested_map (Mock): Mocked `access_nested_map` function.

        Validates:
            - `has_license` returns the expected result.
        """
        mock_access_nested_map.return_value = repo.get("license", {}).get
        ("key")
        client = GithubOrgClient("test_org")
        result = client.has_license(repo, license_key)
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()

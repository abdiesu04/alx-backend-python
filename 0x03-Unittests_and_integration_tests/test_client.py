#!/usr/bin/env python3
import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", {"login": "google"}),
        ("abc", {"login": "abc"})
    ])
    @patch("client.get_json")
    def test_org(self, mock_get_json, org_name, expected_output):
        mock_get_json.return_value = expected_output

        client = GithubOrgClient(org_name)
        result = client.org
        self.assertEqual(result, expected_output)
        mock_get_json.assert_called_once_with(f"https://api.github.com/orgs/{org_name}")

    @parameterized.expand([
        ("google", "https://api.github.com/orgs/google/repos"),
        ("abc", "https://api.github.com/orgs/abc/repos")
    ])
    @patch("client.GithubOrgClient.org", new_callable=Mock)
    def test_public_repos_url(self, mock_org, org_name, expected_url):
        mock_org.return_value = {"repos_url": expected_url}

        client = GithubOrgClient(org_name)
        result = client._public_repos_url
        self.assertEqual(result, expected_url)

    @patch("client.get_json")
    @patch("client.GithubOrgClient._public_repos_url", new_callable=Mock)
    def test_repos_payload(self, mock_public_repos_url, mock_get_json):
        mock_public_repos_url.return_value = "https://api.github.com/orgs/google/repos"
        mock_get_json.return_value = [{"name": "repo1"}, {"name": "repo2"}]

        client = GithubOrgClient("google")
        result = client.repos_payload
        self.assertEqual(result, [{"name": "repo1"}, {"name": "repo2"}])
        mock_get_json.assert_called_once_with("https://api.github.com/orgs/google/repos")

    @patch("client.GithubOrgClient.repos_payload", new_callable=Mock)
    def test_public_repos(self, mock_repos_payload):
        mock_repos_payload.return_value = [
            {"name": "repo1", "license": {"key": "mit"}},
            {"name": "repo2", "license": {"key": "apache-2.0"}},
            {"name": "repo3", "license": {"key": "mit"}}
        ]

        client = GithubOrgClient("google")
        result = client.public_repos()
        self.assertEqual(result, ["repo1", "repo2", "repo3"])

        result = client.public_repos(license="mit")
        self.assertEqual(result, ["repo1", "repo3"])

    @parameterized.expand([
        ({"license": {"key": "mit"}}, "mit", True),
        ({"license": {"key": "apache-2.0"}}, "mit", False),
        ({}, "mit", False)
    ])
    def test_has_license(self, repo, license_key, expected_result):
        result = GithubOrgClient.has_license(repo, license_key)
        self.assertEqual(result, expected_result)

if __name__ == "__main__":
    unittest.main()

import unittest
from unittest.mock import Mock, patch
from parameterized import parameterized
from client import GithubOrgClient

class TestGithubOrgClient(unittest.TestCase):
    @parameterized.expand([
        ("google", "Google"),
        ("abc", "abc")
    ])
    @patch("client.get_json")
    def test_org(self, mock_get_json, input, output):
        mock_get_json.return_value = output

        result = GithubOrgClient.org(input)
        self.assertEqual(result, output)



if __name__ == "__main__":
    unittest.main()

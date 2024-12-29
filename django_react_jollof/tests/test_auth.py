import unittest
from unittest.mock import patch, mock_open

import click

from django_react_jollof.auth import get_client_secrets, write_env_file


class TestAuthFunctions(unittest.TestCase):

    @patch("builtins.open", new_callable=mock_open)
    def test_write_env_file(self, mock_file):
        # Sample secrets dictionary
        secrets = {
            "GOOGLE_CLIENT_ID": "fake-google-client-id",
            "GOOGLE_CLIENT_SECRET": "fake-google-client-secret",
        }

        # Call the function to write the .env file
        write_env_file(secrets)

        # Assert file was opened correctly
        mock_file.assert_called_once_with(".env", "w")

        # Get the handle to the file
        handle = mock_file()

        # Get all write calls
        write_calls = handle.write.call_args_list
        print(f"Debug - Write calls made: {write_calls}")

        # Convert the calls to actual strings that were written
        actual_writes = [args[0][0] for args in write_calls]
        print(f"Debug - Actual writes: {actual_writes}")

        # Expected writes (in any order)
        expected_writes = [
            "GOOGLE_CLIENT_ID=fake-google-client-id\n",
            "GOOGLE_CLIENT_SECRET=fake-google-client-secret\n",
        ]

        # Compare as sets to ignore order
        self.assertEqual(
            set(expected_writes),
            set(actual_writes),
            f"\nExpected writes: {expected_writes}\nActual writes: {actual_writes}",
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_write_env_file_empty_secrets(self, mock_file):
        secrets = {}
        write_env_file(secrets)

        mock_file.assert_called_once_with(".env", "w")
        handle = mock_file()
        self.assertEqual(handle.write.call_count, 0)

    @patch("click.prompt")
    def test_get_client_secrets_google(self, mock_prompt):
        # Set up mock return values for the prompts
        mock_prompt.side_effect = [
            "fake-google-client-id",  # First prompt for Client ID
            "fake-google-client-secret",  # Second prompt for Client Secret
        ]

        # Call the function with 'google' as social login option
        secrets = get_client_secrets("google")

        # Assert that click.prompt was called exactly twice
        self.assertEqual(mock_prompt.call_count, 2)

        # Verify the first prompt call (Client ID)
        mock_prompt.assert_any_call(
            "Enter Google Client ID", default="", show_default=False
        )

        # Verify the second prompt call (Client Secret)
        mock_prompt.assert_any_call(
            "Enter Google Client Secret",
            default="",
            hide_input=True,
            show_default=False,
        )

        # Check that the returned secrets dictionary contains the expected values
        expected_secrets = {
            "GOOGLE_CLIENT_ID": "fake-google-client-id",
            "GOOGLE_CLIENT_SECRET": "fake-google-client-secret",
        }
        self.assertEqual(secrets, expected_secrets)

    def test_get_client_secrets_unsupported(self):
        # Test with an unsupported social login option
        secrets = get_client_secrets("unsupported_provider")

        # Should return an empty dictionary
        self.assertEqual(secrets, {})

    @patch("click.prompt")
    def test_get_client_secrets_empty_input(self, mock_prompt):
        # Set up mock to return empty strings
        mock_prompt.side_effect = ["", ""]

        # Call the function
        secrets = get_client_secrets("google")

        # Verify the returned dictionary contains empty strings
        expected_secrets = {"GOOGLE_CLIENT_ID": "", "GOOGLE_CLIENT_SECRET": ""}
        self.assertEqual(secrets, expected_secrets)

    @patch("click.prompt")
    def test_get_client_secrets_exception_handling(self, mock_prompt):
        # Simulate a Ctrl+C or other abort scenario
        mock_prompt.side_effect = click.Abort()

        # Check if the function handles the exception gracefully
        with self.assertRaises(click.Abort):
            get_client_secrets("google")


if __name__ == "__main__":
    unittest.main()

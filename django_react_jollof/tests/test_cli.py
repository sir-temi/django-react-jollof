import unittest
from unittest.mock import patch, MagicMock, call, ANY
from click.testing import CliRunner

from django_react_jollof.cli import cli, scaffold_project
from django_react_jollof.backend import modify_urls_py


class TestCLI(unittest.TestCase):
    """Test suite for the Django React Jollof CLI."""

    @patch("django_react_jollof.cli.scaffold_project")
    def test_cook_command(self, mock_scaffold_project):
        """Test the `cook` command."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            [
                "cook",
                "--name",
                "TestProject",
                "--frontend",
                "1",
                "--social-login",
                "1",
            ],
        )

        self.assertEqual(result.exit_code, 0)
        mock_scaffold_project.assert_called_once_with(
            "TestProject", "bootstrap", "google"
        )

    def test_cook_invalid_frontend(self):
        """Test the `cook` command with invalid frontend input."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            [
                "cook",
                "--name",
                "TestProject",
                "--frontend",
                "3",  # Invalid frontend option
                "--social-login",
                "1",
            ],
        )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn(
            "Invalid choice '3'! Please choose a valid number option.",
            result.output,
        )

    def test_cook_invalid_social_login(self):
        """Test the `cook` command with invalid social login input."""
        runner = CliRunner()

        result = runner.invoke(
            cli,
            [
                "cook",
                "--name",
                "TestProject",
                "--frontend",
                "1",
                "--social-login",
                "3",  # Invalid social login option
            ],
        )

        self.assertNotEqual(result.exit_code, 0)
        self.assertIn(
            f"Invalid choice '3'! Please choose a valid number option", result.output
        )

    @patch("django_react_jollof.backend.write_env_file")  # Mock write_env_file
    @patch("django_react_jollof.backend.get_client_secrets")  # Mock get_client_secrets
    @patch("django_react_jollof.backend.subprocess.run")  # Mock subprocess.run
    @patch("django_react_jollof.backend.modify_urls_py")  # Mock modify_urls_py
    @patch(
        "django_react_jollof.backend.run_subprocess_command"
    )  # Mock subprocess commands
    @patch("os.makedirs")  # Mock directory creation
    @patch("os.chdir")  # Mock directory change
    @patch("django_react_jollof.backend.copy_templates")  # Mock template copying
    @patch("django_react_jollof.cli.scaffold_frontend")  # Mock scaffold_frontend
    def test_scaffold_project(
        self,
        mock_scaffold_frontend,
        mock_copy_templates,
        mock_chdir,
        mock_makedirs,
        mock_run_subprocess_command,
        mock_modify_urls_py,
        mock_subprocess_run,
        mock_get_secrets,
        mock_write_env_file,
    ):
        """Test the `scaffold_project` function."""

        # Set return values for mocked functions
        mock_modify_urls_py.return_value = None
        mock_copy_templates.return_value = None
        mock_run_subprocess_command.return_value = None
        mock_scaffold_frontend.return_value = None
        mock_subprocess_run.return_value = MagicMock()
        mock_get_secrets.return_value = {
            "GOOGLE_CLIENT_ID": "test_id",
            "GOOGLE_CLIENT_SECRET": "test_secret",
        }

        # Execute the function
        scaffold_project("TestProject", "bootstrap", "google")

        # Assertions for directory operations
        mock_makedirs.assert_called_once_with("TestProject", exist_ok=True)
        mock_chdir.assert_has_calls(
            [call("TestProject"), call("backend"), call("..")], any_order=False
        )

        # Assertions for backend operations
        mock_copy_templates.assert_called_once_with(ANY, ANY, "backend")

        # Assertions for backend subprocess calls
        expected_calls = [
            call(
                ["django-admin", "startproject", "backend"],
                "Django project 'backend' created successfully.",
                "Failed to create Django project 'backend'",
            ),
            call(
                ["pip", "install", "--upgrade", "pip"],
                "Pip upgraded successfully.",
                "Failed to upgrade pip",
            ),
            call(
                [
                    "pip",
                    "install",
                    "djangorestframework",
                    "djangorestframework-simplejwt",
                    "django-cors-headers",
                    "django-allauth",
                    "python-decouple",
                ],
                "Backend dependencies installed successfully.",
                "Failed to install backend dependencies",
            ),
        ]
        mock_run_subprocess_command.assert_has_calls(expected_calls, any_order=True)

        mock_modify_urls_py.assert_called_once_with(ANY)

        # Assertions for secrets and env file
        mock_write_env_file.assert_called_once_with(
            {
                "GOOGLE_CLIENT_ID": "test_id",
                "GOOGLE_CLIENT_SECRET": "test_secret",
            }
        )

        # Assertions for frontend operations
        mock_scaffold_frontend.assert_called_once_with(
            ANY,
            "bootstrap",
            "google",
            "TestProject",
            {"GOOGLE_CLIENT_ID": "test_id", "GOOGLE_CLIENT_SECRET": "test_secret"},
        )

        # Assertions for mocked subprocess
        mock_subprocess_run.assert_any_call(
            ["python", "manage.py", "migrate"], check=True, text=True
        )

    def test_help_command(self):
        """Test the `help` command."""
        runner = CliRunner()
        result = runner.invoke(cli, ["help"])

        self.assertEqual(result.exit_code, 0)
        self.assertIn(
            "Use this CLI to scaffold your boilerplate project", result.output
        )


if __name__ == "__main__":
    unittest.main()

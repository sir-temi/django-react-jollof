import unittest
from unittest.mock import patch, mock_open, MagicMock, call
import subprocess
from django_react_jollof.backend import (
    run_subprocess_command,
    modify_urls_py,
    update_settings,
    scaffold_backend,
)


class TestBackendFunctions(unittest.TestCase):

    def setUp(self):
        self.test_command = ["test", "command"]
        self.success_msg = "Success"
        self.error_msg = "Error"

    def test_run_subprocess_command_success(self):
        """Test successful subprocess command execution"""
        mock_result = MagicMock()
        mock_result.stdout = "Command output"

        with patch("subprocess.run", return_value=mock_result) as mock_run:
            with patch("click.echo") as mock_echo:
                run_subprocess_command(
                    self.test_command, self.success_msg, self.error_msg
                )

                mock_run.assert_called_once_with(
                    self.test_command, check=True, text=True, capture_output=True
                )
                mock_echo.assert_has_calls(
                    [call(self.success_msg), call("Command output")]
                )

    def test_run_subprocess_command_failure(self):
        """Test subprocess command failure"""
        mock_error = subprocess.CalledProcessError(1, self.test_command)
        mock_error.stderr = "Error output"

        with patch("subprocess.run", side_effect=mock_error) as mock_run:
            with patch("click.echo") as mock_echo:
                with patch("sys.exit") as mock_exit:
                    run_subprocess_command(
                        self.test_command, self.success_msg, self.error_msg
                    )

                    mock_echo.assert_called_once_with(f"{self.error_msg}: Error output")
                    mock_exit.assert_called_once_with(1)

    @patch("os.path.join", return_value="mocked_path/urls.py")
    @patch("builtins.open", new_callable=mock_open)
    def test_modify_urls_py_success(self, mock_open, mock_path_join):
        """Test successful modification of urls.py"""
        # Existing content in urls.py
        mock_content = "Original content"

        # Expected content to be written
        expected_content = [
            "from django.contrib import admin\n",
            "from django.urls import path, include\n",
            "\n",
            "urlpatterns = [\n",
            '    path("admin/", admin.site.urls),\n',
            '    path("api/", include("users.urls")), # Added by django-react-jollof\n',
            "]\n",
        ]

        # Mock the file read to return existing content
        mock_open.return_value.read.return_value = mock_content
        mock_open.return_value.readlines.return_value = mock_content.splitlines()

        # Call the function
        modify_urls_py("test_project")

        # Verify open was called correctly
        mock_open.assert_any_call("mocked_path/urls.py", "r")  # Reading the file
        mock_open.assert_any_call("mocked_path/urls.py", "w")  # Writing the file

        # Get the file handle for write operations
        file_handle = mock_open()

        # Verify write calls
        file_handle.writelines.assert_called_once_with(expected_content)

    def test_modify_urls_py_error(self):
        """Test error handling in modify_urls_py"""
        with patch("builtins.open", side_effect=Exception("Test error")):
            with patch("click.echo") as mock_echo:
                with self.assertRaises(Exception):
                    modify_urls_py("test_dir")
                    mock_echo.assert_called_with("Error modifying urls.py: Test error")

    def test_update_settings_no_social_login(self):
        """Test settings update without social login"""
        with patch("os.path.isfile", return_value=True):
            with patch("builtins.open", mock_open()) as mock_file:
                with patch("click.echo") as mock_echo:
                    update_settings("none")

                    # Verify file was opened in append mode
                    mock_file.assert_called_once_with("backend/settings.py", "a")

                    # Verify content written
                    handle = mock_file()
                    self.assertTrue(handle.write.called)
                    # Verify required content is in the writes
                    written_content = "".join(
                        call_args[0][0] for call_args in handle.write.call_args_list
                    )
                    self.assertIn("INSTALLED_APPS", written_content)
                    self.assertNotIn("SOCIALACCOUNT_PROVIDERS", written_content)

    @patch("os.chdir")
    @patch("subprocess.run")
    @patch("click.echo")
    @patch("django_react_jollof.backend.run_subprocess_command")
    @patch("django_react_jollof.backend.copy_templates")
    @patch("django_react_jollof.backend.get_client_secrets")
    @patch("django_react_jollof.backend.modify_urls_py")
    @patch("django_react_jollof.backend.update_settings")
    def test_scaffold_backend_success(
        self,
        mock_update_settings,
        mock_modify_urls,
        mock_get_secrets,
        mock_copy_templates,
        mock_run_command,
        mock_echo,
        mock_subprocess_run,
        mock_chdir,
    ):
        """Test successful backend scaffolding"""
        # Setup subprocess.run mock to handle migrations
        mock_subprocess_run.return_value = MagicMock(returncode=0)
        mock_get_secrets.return_value = {"GOOGLE_CLIENT_ID": "test_id"}

        result = scaffold_backend("template_dir", "google")

        # Verify steps were called in correct order
        mock_run_command.assert_called()
        mock_chdir.assert_has_calls([call("backend"), call("..")])
        mock_modify_urls.assert_called_once()
        mock_copy_templates.assert_called_once()
        self.assertEqual(result, {"GOOGLE_CLIENT_ID": "test_id"})

    @patch("os.chdir")
    @patch("click.echo")
    @patch("sys.exit")
    def test_scaffold_backend_directory_error(self, mock_exit, mock_echo, mock_chdir):
        """Test backend scaffolding with directory error"""
        mock_chdir.side_effect = FileNotFoundError()

        scaffold_backend("template_dir", "none")

        mock_echo.assert_called_with(
            "Template directory 'template_dir/backend' does not exist."
        )


if __name__ == "__main__":
    unittest.main()

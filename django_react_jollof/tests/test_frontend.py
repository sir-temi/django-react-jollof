import os
import shutil
import unittest
from unittest.mock import call, patch, MagicMock, mock_open
import json
from django_react_jollof.frontend import (
    check_node_version,
    scaffold_frontend,
    setup_auth_buttons,
    replace_placeholder_in_file,
    finalise_setup,
    update_package_json,
)


class TestFrontendFunctions(unittest.TestCase):
    def setUp(self):
        """Set up required directories and files for tests."""
        os.makedirs("test_templates/frontend", exist_ok=True)
        os.makedirs("test_templates/helper_files/navbar", exist_ok=True)

        # Create placeholder files required for the test
        with open("test_templates/helper_files/navbar/BootstrapNavbar.jsx", "w") as f:
            f.write("// Placeholder for BootstrapNavbar.jsx")
        with open("test_templates/helper_files/gitignore.txt", "w") as f:
            f.write("# Placeholder for .gitignore")
        with open("test_templates/helper_files/LICENSE", "w") as f:
            f.write("MIT License")
        with open("test_templates/helper_files/README.md", "w") as f:
            f.write("# Placeholder for README")
        with open("test_templates/helper_files/eslintrc.json", "w") as f:
            f.write("{}")

    def tearDown(self):
        """Clean up the created test directories and files."""
        shutil.rmtree("test_templates", ignore_errors=True)

    @patch("subprocess.run")
    def test_check_node_version_success(self, mock_run):
        """Test successful Node.js version check."""
        mock_run.return_value.stdout = "v20.0.0"
        check_node_version()
        mock_run.assert_called_once_with(
            ["node", "--version"], capture_output=True, text=True, check=True
        )

    @patch("subprocess.run")
    def test_check_node_version_failure(self, mock_run):
        """Test Node.js version check failure."""
        mock_run.return_value.stdout = "v18.0.0"
        with self.assertRaises(SystemExit):
            check_node_version()

    @patch("django_react_jollof.frontend.shutil.copy")
    @patch("os.getcwd", return_value="frontend")
    @patch("django_react_jollof.frontend.copy_template_file")  # Mock copy_template_file
    @patch("django_react_jollof.frontend.write_to_env_file")
    @patch("django_react_jollof.frontend.setup_auth_buttons")
    @patch("django_react_jollof.frontend.replace_placeholder_in_file")
    @patch("django_react_jollof.frontend.update_package_json")
    @patch("django_react_jollof.frontend.copy_templates")
    @patch("django_react_jollof.frontend.delete_file")  # Mock delete_file
    @patch("os.makedirs")
    @patch("os.chdir")
    @patch("subprocess.run")
    @patch("django_react_jollof.frontend.check_node_version")
    def test_scaffold_frontend(
        self,
        mock_check_node_version,
        mock_run,
        mock_chdir,
        mock_makedirs,
        mock_delete_file,
        mock_copy_templates,
        mock_update_package_json,
        mock_replace_placeholder_in_file,
        mock_setup_auth_buttons,
        mock_write_to_env_file,
        mock_copy_template_file,
        mock_getcwd,
        mock_copy,
    ):
        """Test the full scaffold_frontend function with mocks."""
        # Mock Node.js version check to always pass
        mock_check_node_version.return_value = None

        # Mock subprocess calls
        mock_run.return_value = MagicMock()

        # Mock directory operations
        mock_chdir.return_value = None
        mock_makedirs.return_value = None

        # Mock file operations
        mock_copy_templates.return_value = None
        mock_delete_file.return_value = None
        mock_update_package_json.return_value = None
        mock_replace_placeholder_in_file.return_value = None
        mock_setup_auth_buttons.return_value = None
        mock_write_to_env_file.return_value = None
        mock_copy_template_file.return_value = None
        mock_copy.return_value = None

        # Test parameters
        template_dir = "test_templates"
        frontend = "bootstrap"
        social_login = "google"
        project_name = "TestProject"

        # Execute the function under test
        try:
            scaffold_frontend(template_dir, frontend, social_login, project_name)
        except SystemExit:
            self.fail("scaffold_frontend raised SystemExit unexpectedly!")

        # Assertions for Node.js version check
        mock_check_node_version.assert_called_once()

        # Assertions for subprocess calls
        mock_run.assert_any_call(
            ["npm", "create", "vite@4.4.0", "frontend", "--", "--template", "react"],
            check=True,
            text=True,
        )
        mock_run.assert_any_call(["npm", "install"], check=True, text=True)

        # Assertions for directory operations
        mock_chdir.assert_any_call("frontend")
        mock_makedirs.assert_any_call("src/components", exist_ok=True)

        # Assertions for template copying
        mock_copy_templates.assert_called_once_with(
            f"{template_dir}/frontend", os.getcwd(), "frontend"
        )

        # Assert Navbar template was copiied
        mock_copy.assert_has_calls(
            [
                call(
                    "test_templates/helper_files/navbar/BootstrapNavbar.jsx",
                    "src/components/Navbar.jsx",
                )
            ]
        )

        # Assertions for file deletion
        expected_delete_calls = [
            call("frontend/.gitignore"),
            call("frontend/.eslintrc.cjs"),
            call("frontend/src/App.css"),
            call("frontend/src/index.css"),
        ]
        mock_delete_file.assert_has_calls(expected_delete_calls, any_order=True)

        # Assertions for copying specific files
        mock_copy_template_file.assert_any_call(
            f"{template_dir}/helper_files/gitignore.txt",
            "frontend/.gitignore",
            ".gitignore file",
        )
        mock_copy_template_file.assert_any_call(
            f"{template_dir}/helper_files/eslintrc.json",
            "frontend/frontend/.eslintrc.json",
            ".eslintrc.json file",
        )

        # Assertions for package.json updates
        mock_update_package_json.assert_called_once_with(
            "package.json", {"react-bootstrap": "^2.7.4", "bootstrap": "^5.2.3"}
        )

        # Assertions for placeholder replacements
        mock_replace_placeholder_in_file.assert_any_call(
            "frontend/index.html", "{{ PROJECT_NAME }}", project_name
        )
        mock_replace_placeholder_in_file.assert_any_call(
            "src/components/Navbar.jsx", "{{ PROJECT_NAME }}", project_name
        )

        # Assertions for authentication buttons setup
        mock_setup_auth_buttons.assert_called_once_with(template_dir, social_login)

        # Assertions for writing to .env file
        mock_write_to_env_file.assert_called_once_with(social_login, None)

    @patch(
        "builtins.open",
        new_callable=mock_open,
        read_data="Placeholder: {{ PROJECT_NAME }}",
    )
    @patch(
        "os.path.isfile", return_value=True
    )  # Mock os.path.isfile to always return True
    def test_replace_placeholder_in_file(self, mock_isfile, mock_open_func):
        """Test placeholder replacement in a file."""
        file_path = "test_file.txt"

        # Call the function
        replace_placeholder_in_file(file_path, "{{ PROJECT_NAME }}", "TestProject")

        # Assert file read and write
        mock_open_func.assert_any_call(file_path, "r")
        mock_open_func.assert_any_call(file_path, "w")

        # Assert content written
        file_handle = mock_open_func()
        file_handle.write.assert_called_once_with("Placeholder: TestProject")

    @patch("os.makedirs")
    @patch("shutil.copy")
    def test_setup_auth_buttons(self, mock_copy, mock_makedirs):
        """Test setup of social login buttons."""
        template_dir = "test_templates"
        setup_auth_buttons(template_dir, "google")

        # Assert directory creation
        mock_makedirs.assert_called_once_with(
            "src/components/auth_buttons", exist_ok=True
        )

        # Assert button files copying
        mock_copy.assert_any_call(
            "test_templates/helper_files/auth_buttons/AuthButtons.jsx",
            "src/components/auth_buttons/AuthButtons.jsx",
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/auth_buttons/GoogleLoginButton.jsx",
            "src/components/auth_buttons/GoogleLoginButton.jsx",
        )

    @patch("os.getcwd", return_value="test_templates")
    @patch("shutil.copy")
    def test_finalise_setup(self, mock_copy, mock_getcwd):
        """Test finalizing setup by generating additional files."""
        template_dir = "test_templates"

        # Test with Bootstrap frontend
        finalise_setup(template_dir, "bootstrap")

        # Validate that required files are being copied
        mock_copy.assert_any_call(
            "test_templates/helper_files/gitignore.txt",
            os.path.join("test_templates", ".gitignore"),
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/LICENSE", os.path.join(template_dir, "LICENSE")
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/README.md",
            os.path.join(template_dir, "README.md"),
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/eslintrc.json",
            os.path.join(template_dir, "frontend/.eslintrc.json"),
        )

        # Ensure Material framework-specific files are not copied for Bootstrap
        self.assertNotIn(
            call(
                "test_templates/helper_files/mui/mui_main.jsx",
                os.path.join(template_dir, "frontend/src/main.jsx"),
            ),
            mock_copy.call_args_list,
        )

        # Reset mock for the Material framework test
        mock_copy.reset_mock()

        # Test with Material frontend
        finalise_setup(template_dir, "material")

        # Validate that Material framework-specific files are copied
        mock_copy.assert_any_call(
            "test_templates/helper_files/mui/mui_main.jsx",
            os.path.join(template_dir, "frontend/src/main.jsx"),
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/mui/mui_main.css",
            os.path.join(template_dir, "frontend/src/styles/main.css"),
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/mui/Login.jsx",
            os.path.join(template_dir, "frontend/src/pages/Login.jsx"),
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/mui/Register.jsx",
            os.path.join(template_dir, "frontend/src/pages/Register.jsx"),
        )

        # Validate common files are still being copied
        mock_copy.assert_any_call(
            "test_templates/helper_files/gitignore.txt",
            os.path.join(template_dir, ".gitignore"),
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/LICENSE", os.path.join(template_dir, "LICENSE")
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/README.md",
            os.path.join(template_dir, "README.md"),
        )
        mock_copy.assert_any_call(
            "test_templates/helper_files/eslintrc.json",
            os.path.join(template_dir, "frontend/.eslintrc.json"),
        )

    @patch("builtins.open", new_callable=mock_open)
    def test_update_package_json(self, mock_open_func):
        """Test updating package.json."""
        mock_open_func.return_value.read.return_value = '{"dependencies": {}}'
        updates = {"react-router-dom": "^6.0.0"}
        update_package_json("package.json", updates)

        # Assert file read and write
        mock_open_func.assert_any_call("package.json", "r")
        mock_open_func.assert_any_call("package.json", "w")

        # Assert updated JSON structure
        file_handle = mock_open_func()
        written_content = "".join(
            call.args[0] for call in file_handle.write.call_args_list
        )
        self.assertEqual(
            json.loads(written_content),
            {"dependencies": {"react-router-dom": "^6.0.0"}},
        )


if __name__ == "__main__":
    unittest.main()

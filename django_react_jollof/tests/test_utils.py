import unittest
from unittest.mock import patch, mock_open
import os
import shutil
import click
from typing import List
from django_react_jollof.utils import (
    validate_choice,
    copy_templates,
    delete_file,
    FRONTEND_DEPENDENCIES,
)


class TestUtilsFunctions(unittest.TestCase):

    def test_validate_choice_valid_input(self):
        """Test validate_choice with valid inputs"""
        valid_choices = [1, 2, 3]
        self.assertTrue(validate_choice("1", valid_choices))
        self.assertTrue(validate_choice("2", valid_choices))
        self.assertTrue(validate_choice("3", valid_choices))

    def test_validate_choice_invalid_number(self):
        """Test validate_choice with invalid number input"""
        valid_choices = [1, 2, 3]
        with patch("click.secho") as mock_secho:
            self.assertFalse(validate_choice("4", valid_choices))
            mock_secho.assert_called_once()
            self.assertIn("Invalid choice", mock_secho.call_args[0][0])

    def test_validate_choice_non_numeric(self):
        """Test validate_choice with non-numeric input"""
        valid_choices = [1, 2, 3]
        with patch("click.secho") as mock_secho:
            self.assertFalse(validate_choice("abc", valid_choices))
            mock_secho.assert_called_once()
            self.assertIn("not a number", mock_secho.call_args[0][0])

    @patch("os.path.exists")
    @patch("os.walk")
    @patch("os.makedirs")
    @patch("shutil.copy2")
    @patch("click.secho")
    def test_copy_templates_success(
        self, mock_secho, mock_copy2, mock_makedirs, mock_walk, mock_exists
    ):
        """Test successful template copying"""
        # Setup mocks
        mock_exists.return_value = True
        mock_walk.return_value = [
            ("/src", ["dir1"], ["file1.txt"]),
            ("/src/dir1", [], ["file2.txt"]),
        ]

        # Call function
        copy_templates("/src", "/dest", "test-dir")

        # Verify calls
        mock_exists.assert_called_once_with("/src")
        self.assertEqual(mock_copy2.call_count, 2)
        mock_makedirs.assert_called()
        mock_secho.assert_called()

    @patch("os.path.exists")
    def test_copy_templates_source_not_found(self, mock_exists):
        """Test copy_templates with non-existent source directory"""
        mock_exists.return_value = False

        with self.assertRaises(FileNotFoundError):
            copy_templates("/nonexistent", "/dest", "test-dir")

    @patch("os.path.exists")
    @patch("os.walk")
    def test_copy_templates_permission_error(self, mock_walk, mock_exists):
        """Test copy_templates with permission error"""
        mock_exists.return_value = True
        mock_walk.side_effect = PermissionError("Permission denied")

        with self.assertRaises(PermissionError):
            copy_templates("/src", "/dest", "test-dir")

    def test_frontend_dependencies_structure(self):
        """Test the structure of FRONTEND_DEPENDENCIES constant"""
        self.assertIn("bootstrap", FRONTEND_DEPENDENCIES)
        self.assertIn("material", FRONTEND_DEPENDENCIES)

        # Verify bootstrap dependencies
        self.assertIn("react-bootstrap", FRONTEND_DEPENDENCIES["bootstrap"])
        self.assertIn("bootstrap", FRONTEND_DEPENDENCIES["bootstrap"])

        # Verify material dependencies
        self.assertIn("@mui/material", FRONTEND_DEPENDENCIES["material"])
        self.assertIn("@emotion/react", FRONTEND_DEPENDENCIES["material"])
        self.assertIn("@emotion/styled", FRONTEND_DEPENDENCIES["material"])
        self.assertIn("@mui/icons-material", FRONTEND_DEPENDENCIES["material"])

    @patch("os.path.exists")
    @patch("os.remove")
    @patch("click.echo")
    def test_delete_file_success(self, mock_echo, mock_remove, mock_exists):
        """Test successful file deletion"""
        mock_exists.return_value = True

        delete_file("/path/to/file.txt")

        mock_exists.assert_called_once_with("/path/to/file.txt")
        mock_remove.assert_called_once_with("/path/to/file.txt")
        mock_echo.assert_called_once()
        self.assertIn("Successfully deleted", mock_echo.call_args[0][0])

    @patch("os.path.exists")
    @patch("click.echo")
    def test_delete_file_nonexistent(self, mock_echo, mock_exists):
        """Test deletion of non-existent file"""
        mock_exists.return_value = False

        delete_file("/path/to/nonexistent.txt")

        mock_exists.assert_called_once_with("/path/to/nonexistent.txt")
        mock_echo.assert_called_once()
        self.assertIn("does not exist", mock_echo.call_args[0][0])

    @patch("os.path.exists")
    @patch("os.remove")
    @patch("click.echo")
    def test_delete_file_permission_error(self, mock_echo, mock_remove, mock_exists):
        """Test deletion with permission error"""
        mock_exists.return_value = True
        mock_remove.side_effect = PermissionError()

        delete_file("/path/to/protected.txt")

        mock_exists.assert_called_once()
        mock_remove.assert_called_once()
        mock_echo.assert_called_once()
        self.assertIn("Permission denied", mock_echo.call_args[0][0])


if __name__ == "__main__":
    unittest.main()

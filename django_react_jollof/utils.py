import os
import shutil
from typing import List
import click


def validate_choice(choice: str, valid_choices: List[int]) -> bool:
    """
    Validate the choice input to ensure it's a valid number-based option.

    Args:
        choice (str): The user's input choice as a string.
        valid_choices (List[int]): A list of valid integer choices.

    Returns:
        bool: True if the choice is valid, False otherwise.
    """
    try:
        choice_int: int = int(choice)  # Try to convert to integer
    except ValueError:
        click.secho(
            f"Invalid input! '{choice}' is not a number. Please choose a valid option.",
            fg="red",
        )
        return False

    if choice_int not in valid_choices:
        click.secho(
            f"Invalid choice '{choice_int}'! Please choose a valid number option.",
            fg="red",
        )
        return False
    return True


def copy_templates(src: str, dest: str, directory: str) -> None:
    """
    Recursively copy template files from the source directory to the destination directory.

    This function performs the following actions:
    1. Validates the existence of the source directory.
    2. Walks through the source directory and copies files to the destination.
    3. Preserves the directory structure during copying.
    4. Logs the progress and any errors encountered.

    Args:
        src (str): Source directory path containing template files.
        dest (str): Destination directory path where templates will be copied.

    Raises:
        FileNotFoundError: If the source directory does not exist.
        PermissionError: If there are permission issues accessing the directories or files.
        Exception: For any other unforeseen errors during the copying process.
    """
    click.secho(f"Starting to generate templates for {directory}.", fg="yellow")

    if not os.path.exists(src):
        click.secho(f"Source directory '{src}' does not exist.", fg="red")
        raise FileNotFoundError(f"Source directory '{src}' does not exist.")

    try:
        for root, dirs, files in os.walk(src):
            for file in files:
                # Full path of source and destination
                src_file: str = os.path.join(root, file)
                relative_path: str = os.path.relpath(src_file, src)
                dest_file: str = os.path.join(dest, relative_path)

                # Ensure the destination directory exists
                dest_dir: str = os.path.dirname(dest_file)
                os.makedirs(dest_dir, exist_ok=True)

                # Copy the file with metadata
                shutil.copy2(src_file, dest_file)

    except PermissionError as e:
        click.secho(f"Permission denied: {e}", fg="red")
        raise
    except shutil.Error as e:
        click.secho(f"Error copying files: {e}", fg="red")
        raise
    except Exception as e:
        click.secho(f"Unexpected error during template copying: {e}", fg="red")
        raise


FRONTEND_DEPENDENCIES = {
    "bootstrap": {"dependencies": {"react-bootstrap": "^2.7.4", "bootstrap": "^5.2.3"}},
    "material": {
        "dependencies": {
            "@mui/material": "^5.11.6",
            "@emotion/react": "^11.10.6",
            "@emotion/styled": "^11.10.6",
            "@mui/icons-material": "^5.16.13",
        }
    },
}


def delete_file(file_path: str) -> None:
    """
    Delete a file at the specified file path.

    This function attempts to remove the file located at `file_path`. It provides feedback
    on the operation's success or failure using `click.echo`.

    Args:
        file_path (str): The path to the file that needs to be deleted.

    Raises:
        PermissionError: If the script lacks the necessary permissions to delete the file.
        Exception: For any other unexpected errors that occur during the deletion process.
    """
    if os.path.exists(file_path):
        try:
            os.remove(file_path)
            click.echo(f"Successfully deleted {file_path}")
        except PermissionError:
            click.echo(f"Error: Permission denied while deleting {file_path}.")
        except Exception as e:
            click.echo(f"An unexpected error occurred while deleting {file_path}: {e}")
    else:
        click.echo(
            f"Warning: The file {file_path} does not exist and cannot be deleted."
        )

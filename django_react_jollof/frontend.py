import json
import os
import shutil
import subprocess
import sys
from typing import Dict, Optional

import click
import logging

from django_react_jollof.utils import FRONTEND_DEPENDENCIES, copy_templates, delete_file

# Set up logging for better traceability
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Define constants for npm commands
NPM_CREATE_VITE_CMD = [
    "npm",
    "create",
    "vite@4.4.0",
    "frontend",
    "--",
    "--template",
    "react",
]
NPM_INSTALL_CMD = ["npm", "install"]


def check_node_version() -> None:
    """
    Ensure the user has Node.js version 20 or higher.
    Exits the program if the Node.js version is insufficient or Node.js is not installed.
    """
    try:
        # Get the installed Node.js version
        result: subprocess.CompletedProcess = subprocess.run(
            ["node", "--version"], capture_output=True, text=True, check=True
        )
        version_str: str = result.stdout.strip().lstrip("v")
        major_version: int = int(version_str.split(".")[0])

        # Enforce minimum Node.js version 20
        if major_version < 20:
            click.echo(
                f"Error: Node.js version 20 or higher is required. Your version: {version_str}. Please upgrade Node.js."
            )
            sys.exit(1)
    except (subprocess.CalledProcessError, FileNotFoundError, IndexError, ValueError):
        click.echo(
            "Error: Node.js is not installed or has an invalid version. Please install Node.js version 20 or higher."
        )
        sys.exit(1)


def replace_placeholder_in_file(
    file_path: str, placeholder: str, replacement: str
) -> None:
    """Replace a placeholder in a file with a replacement string."""
    if not os.path.isfile(file_path):
        click.echo(f"File '{file_path}' does not exist for placeholder replacement.")
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    try:
        with open(file_path, "r") as file:
            content: str = file.read()

        if placeholder not in content:
            click.echo(
                f"Placeholder '{placeholder}' not found in '{file_path}'. No replacement made."
            )
            return

        updated_content: str = content.replace(placeholder, replacement.title())

        with open(file_path, "w") as file:
            file.write(updated_content)

        click.echo(
            f"Replaced placeholder '{placeholder}' with '{replacement}' in '{file_path}'."
        )
    except Exception as e:
        click.echo(f"Error replacing placeholder in '{file_path}': {e}")
        raise


def copy_template_file(
    template_path: str, destination_path: str, description: str
) -> None:
    """Copy a template file to the destination and handle errors."""
    try:
        shutil.copy(template_path, destination_path)
        click.echo(f"{description} generated successfully.")
    except FileNotFoundError as e:
        click.echo(f"Error: Template file not found - {template_path}: {e}")
        sys.exit(1)
    except PermissionError as e:
        click.echo(f"Permission denied while copying {description}: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error while copying {description}: {e}")
        sys.exit(1)


def scaffold_frontend(
    template_dir: str,
    frontend: str,
    social_login: str,
    project_name: str,
    secrets: Optional[Dict[str, str]] = None,
) -> None:
    """Scaffold the React frontend and install necessary dependencies."""
    try:
        # Step 1: Check Node.js version
        click.echo("Checking Node.js version...")
        check_node_version()
        click.echo("Node.js version is sufficient.")

        # Step 2: Create a new Vite project with React template
        click.echo("Setting up React frontend with Vite...")
        subprocess.run(NPM_CREATE_VITE_CMD, check=True, text=True)
        click.echo("Vite React project 'frontend' created successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to create Vite React project.\nError: {e.stderr.strip()}")
        sys.exit(1)

    try:
        # Step 3: Replace default package.json
        os.chdir("frontend")
        frontend_template_dir: str = os.path.join(template_dir, "frontend")

        click.echo("Copying frontend templates...")
        copy_templates(frontend_template_dir, os.getcwd(), "frontend")

        # Step 4: Delete unnecessary files
        delete_file(os.path.join(os.getcwd(), ".gitignore"))
        delete_file(os.path.join(os.getcwd(), ".eslintrc.cjs"))
        delete_file(os.path.join(os.getcwd(), "src", "App.css"))
        delete_file(os.path.join(os.getcwd(), "src", "index.css"))

        # Step 5: Add frontend dependencies
        if frontend.lower() in FRONTEND_DEPENDENCIES:
            frontend_dependencies = FRONTEND_DEPENDENCIES[frontend.lower()]
            update_package_json("package.json", frontend_dependencies)
        else:
            click.echo(
                f"Unknown frontend framework '{frontend}'. Skipping additional dependencies."
            )

        # Step 6: Install frontend dependencies
        click.echo("Installing frontend dependencies from package.json...")
        subprocess.run(NPM_INSTALL_CMD, check=True, text=True)
        click.echo("Frontend dependencies installed successfully.")

        # Step 7: Replace Project name in index.html and NavBar.jsx
        # based on the selected framework
        click.echo(
            f"Generating index.html and Navbar based on selected frontend framework: {frontend}..."
        )

        replace_placeholder_in_file(
            os.path.join(os.getcwd(), "index.html"), "{{ PROJECT_NAME }}", project_name
        )

        components_dir: str = os.path.join("src", "components")
        os.makedirs(components_dir, exist_ok=True)

        # Set project name in NavBar.jsx
        navbar_template: str = os.path.join(
            template_dir, "helper_files", "navbar", f"{frontend.title()}Navbar.jsx"
        )
        dest_navbar: str = os.path.join(components_dir, "Navbar.jsx")
        shutil.copy(navbar_template, dest_navbar)
        replace_placeholder_in_file(dest_navbar, "{{ PROJECT_NAME }}", project_name)

        click.echo("Navbar component generated successfully.")

        # Step 8: Handle social login buttons if applicable
        if social_login != "none":
            click.echo(
                "Setting up authentication buttons based on social login choice..."
            )
            setup_auth_buttons(template_dir, social_login)

        # Step 9: Write social_login value into .env file
        write_to_env_file(social_login, secrets)

        # Step 10: Finalize setup with additional files (.gitignore, LICENSE, README.md)
        finalise_setup(template_dir, frontend)

    except Exception as e:
        click.echo(f"Unexpected error during frontend scaffolding: {e}")
        sys.exit(1)


def setup_auth_buttons(template_dir: str, social_login: str) -> None:
    """Handle setup of social login buttons."""
    auth_buttons_template_dir: str = os.path.join(
        template_dir, "helper_files", "auth_buttons"
    )
    dest_auth_buttons_dir: str = os.path.join("src", "components", "auth_buttons")
    os.makedirs(dest_auth_buttons_dir, exist_ok=True)

    main_auth_button_template: str = os.path.join(
        auth_buttons_template_dir, "AuthButtons.jsx"
    )
    shutil.copy(
        main_auth_button_template,
        os.path.join(dest_auth_buttons_dir, "AuthButtons.jsx"),
    )

    social_login_button_template: str = os.path.join(
        auth_buttons_template_dir, f"{social_login.title()}LoginButton.jsx"
    )
    shutil.copy(
        social_login_button_template,
        os.path.join(dest_auth_buttons_dir, f"{social_login.title()}LoginButton.jsx"),
    )
    click.echo(f"{social_login} login button set up.")


def write_to_env_file(social_login: str, secrets: Optional[Dict[str, str]]) -> None:
    """Write the social login information to the .env file."""
    with open(".env", "w") as env_file:
        env_file.write(f"VITE_SOCIAL_LOGIN={social_login}\n")

        if social_login == "google" and secrets:
            env_file.write(
                f'VITE_GOOGLE_CLIENT_ID={secrets.get("GOOGLE_CLIENT_ID", "")}\n'
            )
            env_file.write(
                f'VITE_GOOGLE_CLIENT_SECRET={secrets.get("VITE_GOOGLE_CLIENT_SECRET", "")}\n'
            )

    click.echo(".env file created with social_login configuration.")

    os.chdir("..")
    click.echo("Returned to the project root directory.")


def finalise_setup(template_dir: str, frontend: str) -> None:
    """Finalize the project setup by generating necessary files."""
    click.echo("Generating .gitignore, LICENSE, and README.md files...")

    current_dir = os.getcwd()
    src_dir = os.path.join(current_dir, "frontend", "src")
    helper_files_dir = os.path.join(template_dir, "helper_files")

    # Generate .gitignore
    copy_template_file(
        os.path.join(helper_files_dir, "gitignore.txt"),
        os.path.join(current_dir, ".gitignore"),
        ".gitignore file",
    )

    # Generate LICENSE
    copy_template_file(
        os.path.join(helper_files_dir, "LICENSE"),
        os.path.join(current_dir, "LICENSE"),
        "LICENSE file",
    )

    # Generate README.md
    copy_template_file(
        os.path.join(helper_files_dir, "README.md"),
        os.path.join(current_dir, "README.md"),
        "README.md file",
    )

    # Generate ESLint file
    copy_template_file(
        os.path.join(helper_files_dir, "eslintrc.json"),
        os.path.join(current_dir, "frontend", ".eslintrc.json"),
        ".eslintrc.json file",
    )

    # Replace main.jsx if bootstrap framework
    # was selected
    if frontend == "material":
        # Copy files for material framework
        copy_template_file(
            os.path.join(helper_files_dir, "mui", "mui_main.jsx"),
            os.path.join(src_dir, "main.jsx"),
            "main.jsx file",
        )

        copy_template_file(
            os.path.join(helper_files_dir, "mui", "mui_main.css"),
            os.path.join(src_dir, "styles", "main.css"),
            "main.css file",
        )

        copy_template_file(
            os.path.join(helper_files_dir, "mui", "Login.jsx"),
            os.path.join(src_dir, "pages", "Login.jsx"),
            "Login.jsx file",
        )

        copy_template_file(
            os.path.join(helper_files_dir, "mui", "Register.jsx"),
            os.path.join(src_dir, "pages", "Register.jsx"),
            "Register.jsx file",
        )


def update_package_json(file_path: str, updates: dict) -> None:
    """Update specific fields in package.json."""
    try:
        with open(file_path, "r") as file:
            package_data = json.load(file)

        # Update dependencies
        if "dependencies" not in package_data:
            package_data["dependencies"] = {}
        package_data["dependencies"].update(updates)

        with open(file_path, "w") as file:
            json.dump(package_data, file, indent=2)

        click.secho("package.json updated successfully.", fg="green", bold=True)
    except json.JSONDecodeError as e:
        click.secho(f"Invalid JSON in package.json: {e}", fg="red", bold=True)
        raise
    except Exception as e:
        click.secho(f"Error updating package.json: {e}", fg="red", bold=True)
        raise

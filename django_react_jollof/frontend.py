import json
import os
import shutil
import subprocess
import sys
from typing import Dict

import click

from django_react_jollof.utils import FRONTEND_DEPENDENCIES, copy_templates, delete_file


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
            click.echo("Error: Node.js version 20 or higher is required.")
            click.echo(
                f"Your Node.js version: {version_str}. Please upgrade Node.js and try again."
            )
            sys.exit(1)
    except subprocess.CalledProcessError:
        click.echo("Error: Failed to retrieve Node.js version.")
        sys.exit(1)
    except FileNotFoundError:
        click.echo(
            "Error: Node.js is not installed. Please install Node.js version 20 or higher."
        )
        sys.exit(1)
    except (IndexError, ValueError):
        click.echo(
            "Error: Unable to parse Node.js version. Ensure Node.js is correctly installed."
        )
        sys.exit(1)


def replace_placeholder_in_file(
    file_path: str, placeholder: str, replacement: str
) -> None:
    """
    Replace a placeholder in a file with a replacement string.

    Args:
        file_path (str): The path to the file where replacement will occur.
        placeholder (str): The placeholder string to be replaced.
        replacement (str): The string to replace the placeholder with.

    Raises:
        FileNotFoundError: If the specified file does not exist.
        IOError: If there's an error reading or writing the file.
    """
    if not os.path.isfile(file_path):
        # logger.error(f"File '{file_path}' does not exist for placeholder replacement.")
        raise FileNotFoundError(f"File '{file_path}' does not exist.")

    try:
        with open(file_path, "r") as file:
            content = file.read()

        if placeholder not in content:
            # logger.warning(f"Placeholder '{placeholder}' not found in '{file_path}'. No replacement made.")
            return

        updated_content = content.replace(placeholder, replacement.title())

        with open(file_path, "w") as file:
            file.write(updated_content)

        # logger.info(f"Replaced placeholder '{placeholder}' with '{replacement}' in '{file_path}'.")
    except Exception as e:
        # logger.error(f"Error replacing placeholder in '{file_path}': {e}")
        raise


def copy_template_file(template_path, destination_path, description):
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
    secrets: Dict,
) -> None:
    """
    Set up the React frontend with a pre-configured package.json, install dependencies,
    copy necessary templates, and configure social login components based on user input.

    Args:
        template_dir (str): The directory containing template files for scaffolding.
        frontend (str): The frontend framework choice (e.g., "bootstrap", "material").
        social_login (str): The social login option selected by the user.
                            Expected values: "google", "github", "both", or "none".

    Raises:
        SystemExit: Exits the program if any subprocess command fails or
                    if file operations encounter errors.
    """
    try:
        # Step 1: Check Node.js version
        click.echo("Checking Node.js version...")
        check_node_version()
        click.echo("Node.js version is sufficient.")

        # Step 2: Create a new Vite project with React template
        click.echo("Setting up React frontend with Vite...")
        subprocess.run(
            ["npm", "create", "vite@4.4.0", "frontend", "--", "--template", "react"],
            check=True,
            text=True,
        )
        click.echo("Vite React project 'frontend' created successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(f"Failed to create Vite React project.\nError: {e.stderr.strip()}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error during Vite project creation: {e}")
        sys.exit(1)

    try:
        # Step 3: Replace the default package.json with the pre-configured one
        os.chdir("frontend")
        frontend_template_dir: str = os.path.join(template_dir, "frontend")

        try:
            # Step 5: Copy templates for frontend
            click.echo("Copying frontend templates...")
            copy_templates(frontend_template_dir, os.getcwd(), "frontend")

            # Delete gitignore
            delete_file(os.path.join(os.getcwd(), ".gitignore"))

            # Delete default ESLint file
            delete_file(os.path.join(os.getcwd(), ".eslintrc.cjs"))

            # Delete default Apps.css file
            delete_file(os.path.join(os.getcwd(), "src", "App.css"))

            # Delete default index.css file
            delete_file(os.path.join(os.getcwd(), "src", "index.css"))

            click.echo("Frontend templates generated successfully.")

        except FileNotFoundError as e:
            click.echo(f"Template directory not found: {e}")
            sys.exit(1)
        except PermissionError as e:
            click.echo(f"Permission denied while copying frontend templates: {e}")
            sys.exit(1)
        except Exception as e:
            click.echo(f"Unexpected error during copying frontend templates: {e}")
            sys.exit(1)

        click.secho(
            "Updating package.json with pre-configured package.json...", fg="yellow"
        )

        package_json_file: str = os.path.join(os.getcwd(), "package.json")

        # Add frontend-specific dependencies
        if frontend.lower() in FRONTEND_DEPENDENCIES:
            frontend_dependencies = FRONTEND_DEPENDENCIES[frontend.lower()]
            update_package_json(package_json_file, frontend_dependencies)
        else:
            click.secho(
                f"Unknown frontend framework '{frontend}'. Skipping additional dependencies.",
                fg="yellow",
            )

    except FileNotFoundError as e:
        click.secho(f"File not found during package.json replacement: {e}", fg="red")
        sys.exit(1)
    except PermissionError as e:
        click.secho(f"Permission denied during package.json replacement: {e}", fg="red")
        sys.exit(1)
    except Exception as e:
        click.secho(f"Unexpected error during package.json replacement: {e}", fg="red")
        sys.exit(1)

    try:
        # Step 4: Install dependencies from package.json
        click.echo("Installing frontend dependencies from package.json...")
        subprocess.run(
            ["npm", "install"],
            check=True,
            text=True,
        )
        click.echo("Frontend dependencies installed successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(
            f"Failed to install frontend dependencies.\nError: {e.stderr.strip()}"
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error during frontend dependencies installation: {e}")
        sys.exit(1)

    try:
        # Step 6: Replace Navbar based on the selected framework
        click.secho(
            "Generating Navbar based on selected frontend framework...", fg="yellow"
        )
        components_dir: str = os.path.join("src", "components")
        os.makedirs(components_dir, exist_ok=True)

        helper_files_dir: str = os.path.join(template_dir, "helper_files")
        navbar_template: str = os.path.join(
            helper_files_dir, "navbar", f"{frontend.title()}Navbar.jsx"
        )
        dest_navbar: str = os.path.join(components_dir, "Navbar.jsx")

        if not os.path.isfile(navbar_template):
            click.escho(f"Navbar template not found at '{navbar_template}'.", fg="red")
            sys.exit(1)

        shutil.copy(navbar_template, dest_navbar)

        # Replace main.jsx if bootstrap framework
        # was selected
        if frontend == "material":
            # Copy files for material framework
            copy_template_file(
                os.path.join(helper_files_dir, "mui", "mui_main.jsx"),
                os.path.join("src", "main.jsx"),
                "main.jsx file",
            )

            copy_template_file(
                os.path.join(helper_files_dir, "mui", "mui_main.css"),
                os.path.join("src", "styles", "main.css"),
                "main.css file",
            )

            copy_template_file(
                os.path.join(helper_files_dir, "mui", "Login.jsx"),
                os.path.join("src", "pages", "Login.jsx"),
                "Login.jsx file",
            )

            copy_template_file(
                os.path.join(helper_files_dir, "mui", "Register.jsx"),
                os.path.join("src", "pages", "Register.jsx"),
                "Register.jsx file",
            )

        # Replace the placeholder with the actual project name
        replace_placeholder_in_file(dest_navbar, "{{ PROJECT_NAME }}", project_name)

        click.secho("Navbar component generated successfully.", fg="yellow")

    except FileNotFoundError as e:
        click.echo(f"Navbar template file not found: {e}")
        sys.exit(1)
    except PermissionError as e:
        click.echo(f"Permission denied while replacing Navbar: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error during Navbar replacement: {e}")
        sys.exit(1)

    try:
        # Step 7: Write the social_login value into the .env file
        click.echo("Writing social_login configuration to .env file...")
        with open(".env", "w") as env_file:
            env_file.write(f"VITE_SOCIAL_LOGIN={social_login}\n")

            if secrets:
                env_file.write(
                    f'VITE_GOOGLE_CLIENT_ID={secrets.get("GOOGLE_CLIENT_ID")}\n'
                    f'VITE_GOOGLE_CLIENT_SECRET={secrets.get("VITE_GOOGLE_CLIENT_SECRET")}\n'
                )

        click.echo(".env file created with social_login configuration.")

    except IOError as e:
        click.echo(f"IOError while writing to .env file: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error while writing to .env file: {e}")
        sys.exit(1)

    try:
        # Step 8: Handle authentication buttons based on social login choice
        if social_login.lower() != "none":
            click.echo(
                "Setting up authentication buttons based on social login choice..."
            )
            auth_buttons_template_dir: str = os.path.join(
                template_dir, "helper_files", "auth_buttons"
            )
            dest_auth_buttons_dir: str = os.path.join(
                "src", "components", "auth_buttons"
            )
            os.makedirs(dest_auth_buttons_dir, exist_ok=True)

            main_auth_button_template: str = os.path.join(
                auth_buttons_template_dir, "AuthButtons.jsx"
            )
            dest_main_auth_button: str = os.path.join(
                dest_auth_buttons_dir, "AuthButtons.jsx"
            )

            if not os.path.isfile(main_auth_button_template):
                click.echo(
                    f"AuthButtons.jsx template not found at '{main_auth_button_template}'."
                )
                sys.exit(1)

            shutil.copy(main_auth_button_template, dest_main_auth_button)

            social_login_button_template: str = os.path.join(
                auth_buttons_template_dir, f"{social_login.title()}LoginButton.jsx"
            )
            dest_social_login_button: str = os.path.join(
                dest_auth_buttons_dir, f"{social_login.title()}LoginButton.jsx"
            )

            if not os.path.isfile(social_login_button_template):
                click.echo(
                    f"{social_login.title()}LoginButton.jsx template not found at '{social_login_button_template}'."
                )
                sys.exit(1)

            shutil.copy(social_login_button_template, dest_social_login_button)
        else:
            click.echo("No social login selected. Skipping auth buttons creation.")

    except FileNotFoundError as e:
        click.echo(f"Authentication button template file not found: {e}")
        sys.exit(1)
    except PermissionError as e:
        click.echo(f"Permission denied while copying authentication buttons: {e}")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error during authentication buttons setup: {e}")
        sys.exit(1)

    try:
        # Replace Title in index.html file
        index_template = os.path.join(os.getcwd(), "index.html")
        if os.path.exists(index_template):
            replace_placeholder_in_file(
                index_template, "{{ PROJECT_NAME }}", project_name
            )
        else:
            click.echo(f"Error: Template file not found - {index_template}")
            sys.exit(1)

        os.chdir("..")
        click.echo("Returned to the project root directory.")

        click.secho("Generating .gitignore, LICENSE, and README.md files", fg="yellow")
        current_dir = os.getcwd()

        # Generate .gitignore
        gitignore_template = os.path.join(helper_files_dir, "gitignore.txt")
        copy_template_file(
            gitignore_template,
            os.path.join(current_dir, ".gitignore"),
            ".gitignore file",
        )

        # Generate LICENSE
        licence_template = os.path.join(helper_files_dir, "LICENSE")
        copy_template_file(
            licence_template, os.path.join(current_dir, "LICENSE"), "LICENSE file"
        )

        # Generate README.md
        readme_template = os.path.join(helper_files_dir, "README.md")
        copy_template_file(
            readme_template, os.path.join(current_dir, "README.md"), "README.md file"
        )

        # Generate ESlint file
        eslint_template = os.path.join(helper_files_dir, "eslintrc.json")
        copy_template_file(
            eslint_template,
            os.path.join(current_dir, "frontend", ".eslintrc.json"),
            ".eslintrc.json file",
        )

    except FileNotFoundError as e:
        click.echo(f"Error changing directory back to project root: {e}")
        sys.exit(1)
    except PermissionError as e:
        click.echo(
            f"Permission denied while changing directory back to project root: {e}"
        )
        sys.exit(1)
    except Exception as e:
        click.echo(f"Unexpected error while returning to project root: {e}")
        sys.exit(1)


def update_package_json(file_path: str, updates: dict) -> None:
    """
    Update specific fields in a package.json file.

    Args:
        file_path (str): Path to the package.json file.
        updates (dict): Dictionary containing fields to update.

    Raises:
        FileNotFoundError: If the package.json file does not exist.
        json.JSONDecodeError: If the package.json is not valid JSON.
        IOError: If there's an error reading or writing the file.
    """
    if not os.path.isfile(file_path):
        raise FileNotFoundError(f"package.json not found at '{file_path}'.")

    try:
        with open(file_path, "r") as file:
            package_data = json.load(file)

        # Update the fields
        for key, value in updates.items():
            if key == "dependencies":
                # Update dependencies
                if "dependencies" not in package_data:
                    package_data["dependencies"] = {}

                package_data["dependencies"].update(value)
            else:
                package_data[key] = value

        with open(file_path, "w") as file:
            json.dump(package_data, file, indent=2)

        click.secho("package.json updated successfully.", fg="green", bold=True)
    except json.JSONDecodeError as e:
        click.secho(f"Invalid JSON in package.json: {e}", fg="red", bold=True)
        raise
    except Exception as e:
        click.secho(f"Error updating package.json: {e}", fg="red", bold=True)
        raise

import sys
import os
from textwrap import dedent
from typing import Dict, List
import os
import subprocess

import click

from django_react_jollof.auth import get_client_secrets, write_env_file
from django_react_jollof.utils import copy_templates


def modify_urls_py(project_dir: str) -> None:
    """
    Modifies the main urls.py file to include necessary imports and API URL patterns.

    This function performs the following actions:
    1. Backs up the existing urls.py file.
    2. Reads the current content of urls.py.
    3. Appends required imports and URL patterns if they are not already present.
    4. Writes the updated content back to urls.py.

    Args:
        project_dir (str): The root directory of the project where the backend folder resides.

    Raises:
        FileNotFoundError: If the urls.py file does not exist at the specified path.
        IOError: If there is an error reading or writing to the urls.py file.
    """
    urls_path = os.path.join(project_dir, "backend", "urls.py")

    try:
        # Read the file content
        with open(urls_path, "r") as file:
            lines = file.readlines()

        # Create new content with correct imports
        new_content = [
            "from django.contrib import admin\n",
            "from django.urls import path, include\n",
            "\n",
            "urlpatterns = [\n",
            '    path("admin/", admin.site.urls),\n',
            '    path("api/", include("users.urls")), # Added by django-react-jollof\n',
            "]\n",
        ]

        # Write the new content
        with open(urls_path, "w") as file:
            file.writelines(new_content)

        print("Successfully modified urls.py")

    except Exception as e:
        print(f"Error modifying urls.py: {str(e)}")
        raise


def update_settings(social_login: str) -> None:
    """
    Modify settings.py based on user input to integrate required applications and configurations.

    Args:
        social_login (str): The social login option selected by the user.
                            Expected values: "google", "github", "both", or "none".
    """
    settings_path: str = os.path.join("backend", "settings.py")

    if not os.path.isfile(settings_path):
        click.echo(f"Error: '{settings_path}' does not exist.")
        sys.exit(1)

    try:
        with open(settings_path, "a") as file:
            # Add common configurations
            common_config = dedent(
                """
                # Set by django-react-jollof

                import os

                # Installed apps
                INSTALLED_APPS += [
                    "corsheaders",
                    "rest_framework",
                    "allauth",
                    "allauth.account",
                    "allauth.socialaccount",
                ]

                # Authentication backends
                AUTHENTICATION_BACKENDS = [
                    "allauth.account.auth_backends.AuthenticationBackend",
                ]

                # Site ID
                SITE_ID = 1

                # Django Allauth configuration
                ACCOUNT_EMAIL_REQUIRED = True
                ACCOUNT_USERNAME_REQUIRED = False
                ACCOUNT_AUTHENTICATION_METHOD = "email"
                ACCOUNT_EMAIL_VERIFICATION = "none"

                # Middleware for CORS
                MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
                MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")

                # REST Framework Configuration
                REST_FRAMEWORK = {
                    "DEFAULT_AUTHENTICATION_CLASSES": [
                        "rest_framework_simplejwt.authentication.JWTAuthentication",
                    ],
                    "DEFAULT_PERMISSION_CLASSES": [
                        "rest_framework.permissions.IsAuthenticated",
                    ],
                }

                # CORS Configuration
                CORS_ALLOWED_ORIGINS = [
                    "http://localhost:5173",  # React frontend
                ]
            """
            )
            file.write(common_config)

            # Add social login configurations only if a social login provider is selected
            if social_login != "none":
                # Social account providers section
                social_config_start = dedent(
                    """
                    # Social account providers
                    SOCIALACCOUNT_PROVIDERS = {
                """
                )
                file.write(social_config_start)

                # Google configuration
                if social_login == "google":
                    google_config = dedent(
                        f"""
                        'google': {{
                            'SCOPE': [
                                'profile',
                                'email',
                            ],
                            'AUTH_PARAMS': {{
                                'access_type': 'online',
                            }},
                            'OAUTH_PKCE_ENABLED': True,
                            'APP': {{
                                'client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
                                'secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
                                'key': '',
                            }}
                        }},
                    """
                    )
                    file.write(google_config)

                file.write("}\n")  # Close the SOCIALACCOUNT_PROVIDERS dictionary

            click.echo(f"Updated '{settings_path}' with the selected configurations.")

    except IOError as e:
        click.echo(f"IOError while writing to '{settings_path}': {e}")
        sys.exit(1)


def modify_urls_py(project_dir: str) -> None:
    """
    Modifies the main urls.py file to include necessary imports and API URL patterns.

    This function performs the following actions:
    1. Backs up the existing urls.py file.
    2. Reads the current content of urls.py.
    3. Appends required imports and URL patterns if they are not already present.
    4. Writes the updated content back to urls.py.

    Args:
        project_dir (str): The root directory of the project where the backend folder resides.

    Raises:
        FileNotFoundError: If the urls.py file does not exist at the specified path.
        IOError: If there is an error reading or writing to the urls.py file.
    """
    urls_path = os.path.join(project_dir, "backend", "urls.py")

    try:
        # Read the file content
        with open(urls_path, "r") as file:
            lines = file.readlines()

        # Create new content with correct imports
        new_content = [
            "from django.contrib import admin\n",
            "from django.urls import path, include\n",
            "\n",
            "urlpatterns = [\n",
            '    path("admin/", admin.site.urls),\n',
            '    path("api/", include("users.urls")), # Added by django-react-jollof\n',
            "]\n",
        ]

        # Write the new content
        with open(urls_path, "w") as file:
            file.writelines(new_content)

        print("Successfully modified urls.py")

    except Exception as e:
        print(f"Error modifying urls.py: {str(e)}")
        raise


def scaffold_backend(template_dir: str, social_login: str) -> Dict | None:
    """
    Set up the Django backend by creating the project, installing dependencies,
    configuring settings, and applying migrations.

    Args:
        template_dir (str): The directory containing template files for scaffolding.
        social_login (str): The social login option selected by the user.
                            Expected values: "google", "github", "both", or "none".

    Raises:
        SystemExit: Exits the program if any subprocess command fails or
                    if file operations encounter errors.
    """
    secrets = None

    try:
        click.echo("Setting up Django backend...")

        # Start Django project
        subprocess.run(
            ["django-admin", "startproject", "backend"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        click.echo("Django project 'backend' created successfully.")

    except subprocess.CalledProcessError as e:
        click.echo(
            f"Failed to create Django project 'backend'.\nError: {e.stderr.strip()}"
        )
        sys.exit(1)

    try:
        # Change directory to 'backend'
        os.chdir("backend")
        click.echo("Changed directory to 'backend'.")

    except FileNotFoundError:
        click.echo("Directory 'backend' does not exist.")
        sys.exit(1)
    except PermissionError:
        click.echo("Permission denied while changing directory to 'backend'.")
        sys.exit(1)

    try:
        # Install backend dependencies
        click.echo("Installing backend dependencies...")
        dependencies: List[str] = [
            "djangorestframework",
            "djangorestframework-simplejwt",
            "django-cors-headers",
            "django-allauth",
            "python-decouple",
        ]

        # Upgrade pip first
        click.echo("Upgrading pip...")
        subprocess.run(
            ["pip", "install", "--upgrade", "pip"],
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        click.echo("Pip upgraded successfully.")

        # Install the dependencies
        click.echo(f"Installing dependencies: {', '.join(dependencies)}")
        subprocess.run(
            ["pip", "install"] + dependencies,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )
        click.echo("Backend dependencies installed successfully.")

        # Save the dependencies to requirements.txt for future reference
        click.echo("Saving dependencies to requirements.txt...")
        with open("requirements.txt", "w") as f:
            f.write("\n".join(dependencies))
        click.echo("Dependencies saved to requirements.txt.")

    except subprocess.CalledProcessError as e:
        click.echo(
            f"Failed to install backend dependencies.\nError: {e.stderr.strip()}"
        )
        sys.exit(1)
    except IOError as e:
        click.echo(f"IOError while writing to requirements.txt: {e}")
        sys.exit(1)

    try:
        # Update backend.urls
        click.echo("Modifying backend URLs...")
        modify_urls_py(os.getcwd())

    except Exception as e:
        click.echo(f"Error modifying urls.py: {e}")
        sys.exit(1)

    try:
        # Copy backend templates
        backend_template_dir: str = os.path.join(template_dir, "backend")
        click.echo(f"Copying backend templates from '{backend_template_dir}'...")
        copy_templates(backend_template_dir, os.getcwd(), "backend")
        click.secho("Backend templates generated successfully.", fg="green")

    except FileNotFoundError:
        click.echo(f"Template directory '{backend_template_dir}' does not exist.")
        sys.exit(1)
    except PermissionError:
        click.echo("Permission denied while copying backend templates.")
        sys.exit(1)
    except Exception as e:
        click.echo(f"Error copying backend templates: {e}")
        sys.exit(1)

    if social_login.lower() != "none":
        try:
            # Prompt for client secrets and update settings.py
            click.echo("Prompting for social login client secrets...")
            secrets: Dict[str, str] = get_client_secrets(social_login)
            click.secho("Writing secrets to .env file...", fg="yellow")
            write_env_file(secrets)
            click.secho(".env file created successfully.", fg="yellow")

            # Update settings.py with social login configurations
            click.secho(
                "Updating settings.py with social login configurations...", fg="yellow"
            )
            update_settings(social_login)
            click.secho("settings.py updated successfully.", fg="green")

        except Exception as e:
            click.secho(f"Error handling social login configurations: {e}", fg="red")
            sys.exit(1)

    try:
        # Apply migrations
        click.secho("Running migrations...", fg="yellow")
        subprocess.run(
            ["python", "manage.py", "migrate"],
            check=True,
            text=True,
        )
        click.secho("Migrations applied successfully.", fg="green")

    except subprocess.CalledProcessError as e:
        click.secho(f"Failed to apply migrations.\nError: {e.stderr.strip()}", fg="red")
        sys.exit(1)

    try:
        # Return to project root
        os.chdir("..")
        click.echo("Returned to project root directory.")
        return secrets

    except FileNotFoundError:
        click.secho("Project root directory does not exist.", fg="red")
        sys.exit(1)
    except PermissionError:
        click.secho("Permission denied while changing back to project root.", fg="red")
        sys.exit(1)

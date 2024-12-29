import sys
import os
from textwrap import dedent
from typing import Dict, List, Optional
import subprocess
import click

from django_react_jollof.auth import get_client_secrets, write_env_file
from django_react_jollof.utils import copy_templates, delete_file


def run_subprocess_command(
    command: List[str], success_message: str, error_message: str
) -> None:
    """Helper function to run subprocess commands and handle errors."""
    try:
        result = subprocess.run(command, check=True, text=True, capture_output=True)
        click.echo(success_message)
        click.echo(result.stdout)
    except subprocess.CalledProcessError as e:
        click.echo(f"{error_message}: {e.stderr.strip()}")
        sys.exit(1)


def modify_urls_py(project_dir: str) -> None:
    """Modify urls.py to include necessary imports and API URL patterns."""
    urls_path = os.path.join(project_dir, "backend", "urls.py")

    try:
        with open(urls_path, "r") as file:
            lines = file.readlines()

        new_content = [
            "from django.contrib import admin\n",
            "from django.urls import path, include\n",
            "\n",
            "urlpatterns = [\n",
            '    path("admin/", admin.site.urls),\n',
            '    path("api/", include("users.urls")), # Added by django-react-jollof\n',
            "]\n",
        ]

        with open(urls_path, "w") as file:
            file.writelines(new_content)

        click.echo("Successfully modified urls.py")

    except Exception as e:
        click.echo(f"Error modifying urls.py: {str(e)}")
        raise


def update_settings(social_login: str) -> None:
    """Modify settings.py based on user input to integrate required applications and configurations."""
    settings_path = os.path.join("backend", "settings.py")

    if not os.path.isfile(settings_path):
        click.echo(f"Error: '{settings_path}' does not exist.")
        sys.exit(1)

    try:
        with open(settings_path, "a") as file:
            common_config = dedent(
                """
                # Set by django-react-jollof

                import os

                INSTALLED_APPS += [
                    "corsheaders",
                    "rest_framework",
                    "allauth",
                    "allauth.account",
                    "allauth.socialaccount",
                ]

                AUTHENTICATION_BACKENDS = [
                    "allauth.account.auth_backends.AuthenticationBackend",
                ]

                SITE_ID = 1

                ACCOUNT_EMAIL_REQUIRED = True
                ACCOUNT_USERNAME_REQUIRED = False
                ACCOUNT_AUTHENTICATION_METHOD = "email"
                ACCOUNT_EMAIL_VERIFICATION = "none"

                MIDDLEWARE.insert(0, "corsheaders.middleware.CorsMiddleware")
                MIDDLEWARE.append("allauth.account.middleware.AccountMiddleware")

                REST_FRAMEWORK = {
                    "DEFAULT_AUTHENTICATION_CLASSES": [
                        "rest_framework_simplejwt.authentication.JWTAuthentication",
                    ],
                    "DEFAULT_PERMISSION_CLASSES": [
                        "rest_framework.permissions.IsAuthenticated",
                    ],
                }

                CORS_ALLOWED_ORIGINS = [
                    "http://localhost:5173",  # React frontend
                ]
                """
            )
            file.write(common_config)

            if social_login != "none":
                social_config_start = dedent(
                    """
                    SOCIALACCOUNT_PROVIDERS = {
                """
                )
                file.write(social_config_start)

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

                file.write("}\n")

            click.echo(f"Updated '{settings_path}' with the selected configurations.")

    except IOError as e:
        click.echo(f"IOError while writing to '{settings_path}': {e}")
        sys.exit(1)


def scaffold_backend(template_dir: str, social_login: str) -> Optional[Dict[str, str]]:
    """Set up the Django backend by creating the project, installing dependencies, configuring settings, and applying migrations."""
    secrets = None

    try:
        click.echo("Setting up Django backend...")

        # Start Django project
        run_subprocess_command(
            ["django-admin", "startproject", "backend"],
            "Django project 'backend' created successfully.",
            "Failed to create Django project 'backend'",
        )

        # Change directory to 'backend'
        os.chdir("backend")
        click.echo("Changed directory to 'backend'.")

    except FileNotFoundError:
        click.echo("Directory 'backend' does not exist.")
        sys.exit(1)
    except PermissionError:
        click.echo("Permission denied while changing directory to 'backend'.")
        sys.exit(1)

    # Install backend dependencies
    click.echo("Installing backend dependencies...")
    dependencies = [
        "djangorestframework",
        "djangorestframework-simplejwt",
        "django-cors-headers",
        "django-allauth",
        "python-decouple",
    ]

    run_subprocess_command(
        ["pip", "install", "--upgrade", "pip"],
        "Pip upgraded successfully.",
        "Failed to upgrade pip",
    )

    run_subprocess_command(
        ["pip", "install"] + dependencies,
        "Backend dependencies installed successfully.",
        "Failed to install backend dependencies",
    )

    # Save dependencies to requirements.txt
    click.echo("Saving dependencies to requirements.txt...")
    with open("requirements.txt", "w") as f:
        f.write("\n".join(dependencies))
    click.echo("Dependencies saved to requirements.txt.")

    try:
        # Modify backend.urls
        click.echo("Modifying backend URLs...")
        modify_urls_py(os.getcwd())

    except Exception as e:
        click.echo(f"Error modifying urls.py: {e}")
        sys.exit(1)

    # Copy backend templates
    try:
        backend_template_dir = os.path.join(template_dir, "backend")
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
            # Handle social login
            click.echo("Prompting for social login client secrets...")
            secrets = get_client_secrets(social_login)
            click.secho("Writing secrets to .env file...", fg="yellow")
            write_env_file(secrets)
            click.secho(".env file created successfully.", fg="yellow")

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
        click.secho(f"Failed to apply migrations.\nError: {e.stderr}", fg="red")
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

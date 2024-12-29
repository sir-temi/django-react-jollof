import os
from typing import Dict, List
import click

from django_react_jollof.backend import scaffold_backend
from django_react_jollof.frontend import scaffold_frontend
from django_react_jollof.utils import validate_choice


@click.group()
def cli() -> None:
    """Django React Jollof - CLI to scaffold Django + React projects."""
    pass


@cli.command()
@click.option(
    "--name",
    prompt="Please enter your project name",
    help="The name of your project. This will be used to configure your project setup.",
)
@click.option(
    "--frontend",
    prompt=(
        "Choose the frontend framework for your project:\n"
        "  1. Bootstrap (default)\n"
        "  2. Material Design\n"
        "Select 1 or 2 (default is 1): "
    ),
    default="1",
    help="Choose the frontend framework to use (Bootstrap or Material Design).",
)
@click.option(
    "--social-login",
    prompt=(
        "Select the social login providers you want to integrate:\n"
        "  1. Google\n"
        "  2. No social login (default)\n"
        "Select 1 or 2 (default is 2): "
    ),
    default="2",
    help="Select the social login providers to include in your project.",
)
def cook(name: str, frontend: str, social_login: str) -> None:
    """
    Create a new boilerplate project.

    Args:
        name (str): The name of the project.
        frontend (str): The frontend framework choice as a string.
        social_login (str): The social login option as a string.
    """
    # Define valid choices for frontend and social-login options
    frontend_choices: List[int] = [1, 2]  # 1: Bootstrap, 2: Material Design
    social_login_choices: List[int] = [1, 2]  # 1: Google, 2: None

    # Validate frontend choice
    if not validate_choice(frontend, frontend_choices):
        return  # Exit if invalid frontend choice

    # Validate social login choice
    if not validate_choice(social_login, social_login_choices):
        return  # Exit if invalid social login choice

    # Map numbers to actual values
    frontend_map: Dict[int, str] = {1: "bootstrap", 2: "material"}
    social_login_map: Dict[int, str] = {1: "google", 2: "none"}

    selected_frontend: str = frontend_map[int(frontend)]
    selected_social_login: str = social_login_map[int(social_login)]

    click.secho(
        f"Creating project '{name}' with {selected_frontend} frontend and {selected_social_login} social login...",
        fg="yellow",
    )

    scaffold_project(name, selected_frontend, selected_social_login)


def scaffold_project(name: str, frontend: str, social_login: str) -> None:
    """
    Scaffold the backend and frontend of the project.

    Args:
        name (str): The name of the project.
        frontend (str): The frontend framework choice (e.g., "bootstrap", "material").
        social_login (str): The social login option (e.g., "google", "none", "both").
    """
    template_dir: str = os.path.join(os.path.dirname(__file__), "templates")

    # Create project folder
    os.makedirs(name, exist_ok=True)
    os.chdir(name)

    # Scaffold backend
    secrets = scaffold_backend(template_dir, social_login)

    # Scaffold frontend
    scaffold_frontend(template_dir, frontend, social_login, name, secrets)

    click.secho(f"Project '{name}' created successfully! 🎉", fg="green", bold=True)


@cli.command()
def help():
    """Show help information."""
    click.echo("Use this CLI to scaffold your boilerplate project.")
    click.echo("\nCommands:")
    click.echo("  create    Create a new project")
    click.echo("  help      Show help information")

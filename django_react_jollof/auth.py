from typing import Dict

import click


def get_client_secrets(social_login: str) -> Dict[str, str]:
    """
    Prompt the user to enter client IDs and secrets based on the selected social login providers.

    Args:
        social_login (str): The social login option selected by the user.

    Returns:
        Dict[str, str]: A dictionary containing the entered client IDs and secrets.
    """
    secrets: Dict[str, str] = {}
    if social_login == "google":
        secrets["GOOGLE_CLIENT_ID"] = click.prompt(
            "Enter Google Client ID", default="", show_default=False
        )
        secrets["GOOGLE_CLIENT_SECRET"] = click.prompt(
            "Enter Google Client Secret",
            default="",
            hide_input=True,
            show_default=False,
        )

    return secrets


def write_env_file(secrets: Dict[str, str]) -> None:
    """
    Write the provided client IDs and secrets to a .env file.

    Args:
        secrets (Dict[str, str]): A dictionary containing client IDs and secrets to be written to the .env file.
    """
    with open(".env", "w") as file:
        for key, value in secrets.items():
            if value:
                file.write(f"{key}={value}\n")

    click.echo(".env file created with provided secrets.")

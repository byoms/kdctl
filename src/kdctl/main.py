
import os
from pathlib import Path

import typer
from typing_extensions import Annotated

app = typer.Typer()

def default_kube_config():
    """
    Determine path to the default kubeconfig file for user
    """
    if os.environ.get('HOME'):
        kube_config = f"{os.environ.get('HOME')}/.kube/config"
    else:
        kube_config = None
    
    return kube_config

@app.command("get")
def get_deployment(
    app: Annotated[
        str,
        typer.Argument(
            help="Specify app name"
        ),
    ],
):
    """
    Get Deployment info using app name
    """
    print(f"Placeholder: Return deployment details for {app} [WIP]")

    return None

@app.command("create")
def create_deployment(
    config: Annotated[
        Path,
        typer.Argument(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="Path to the Deployment config file"
        ),
    ],
    kubeconfig: Annotated[
        Path,
        typer.Option(
            exists=True,
            file_okay=True,
            dir_okay=False,
            writable=False,
            readable=True,
            resolve_path=True,
            help="Path to the (Kubernetes) kubeconfig file",
            default_factory=default_kube_config
        )
    ]
):
    """
    Create a Deployment using a config file spec
    """
    text = config.read_text()
    print(f"Config file contents: {text}")

    return


def main():
    app()
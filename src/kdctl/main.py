
import logging
import os
import sys
from pathlib import Path

import yaml
import typer
from kubernetes import client as kclient
from kubernetes import config as kconfig
from kubernetes.client.rest import ApiException
from typing_extensions import Annotated

app = typer.Typer()
logger = logging.getLogger(__name__)

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

    # load config file (yaml) to a dict
    try:
        deploy_config = yaml.safe_load(config.read_bytes())
        logger.debug("Deployment config has valid yaml syntax")
    except yaml.YAMLError as e:
        logger.critical(f"Failed to parse Deployment config. Error: {e}\nQuitting..")
        sys.exit(1)

    return


def main():
    app()
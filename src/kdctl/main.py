
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
        logger.debug("Deployment config has valid yaml syntax, read successful ✓")
        kube_config = yaml.safe_load(kubeconfig.read_bytes())
        logger.debug("kubeconfig has valid yaml syntax, read successful ✓")
    except yaml.YAMLError as e:
        logger.critical(f"Failed to read config file. Error: {e}\nQuitting..")
        sys.exit(1)

    kconf = kclient.Configuration()
    kconfig.load_kube_config_from_dict(
        kube_config,
        client_configuration=kconf
    )
    with kclient.ApiClient(kconf) as api_client:

        app_name = str(deploy_config['name'])
        app_team = str(deploy_config['team'])

        labels = {}
        # the unique label of choice that identifies a deployment
        id_label = {
            "simplismart.ai/app-name": app_name
        }
        labels.update(id_label)
        internal_labels = {
            "simplismart.ai/mgmt": "kdctl",
            "simplismart.ai/team-owner": app_team
        }
        labels.update(internal_labels)
        user_labels = {}
        for label_key, label_value in deploy_config['labels'].items():
            user_labels[f"simplismart.ai/{label_key}"] = label_value
        labels.update(user_labels)

        common_metadata = kclient.V1ObjectMeta(
            name = app_name,
            namespace = app_team,
            labels = labels,
            annotations = {
                "simplismart.ai/app-info": str(deploy_config['description'])
            }
        )

        # define pod spec
        app_ports = []
        app_ports.append(
            kclient.V1ContainerPort(
                name = "app-service",
                container_port = int(deploy_config['port'])
            )
        )
        app_container = kclient.V1Container(
            name = str(deploy_config['name']),
            image = str(deploy_config['image']),
            ports = app_ports
        )
        # can define additional containers here later if needed
        containers = []
        containers.append(app_container)

        pod_spec = kclient.V1PodSpec(
            containers = containers
        )

        # define deployment spec
        label_selector = kclient.V1LabelSelector(
            match_labels = id_label
        )
        template_spec = kclient.V1PodTemplateSpec(
            metadata = common_metadata,
            spec = pod_spec
        )
        deployment_spec = kclient.V1DeploymentSpec(
            replicas = int(deploy_config['replicas']),
            selector = label_selector,
            template = template_spec
        )
        deployment = kclient.V1Deployment(
            metadata = common_metadata,
            spec = deployment_spec
        )

        # namespaces created on a per-team basisa
        namespace = app_team
        body = deployment
        pretty = 'false'
        field_manager = 'simplismart.ai/kdctl'
        field_validation = 'Strict'

        api_instance = kclient.AppsV1Api(api_client)

        try:
            api_response = api_instance.create_namespaced_deployment(
                namespace,
                body,
                pretty=pretty,
                field_manager=field_manager,
                field_validation=field_validation
            )
            logger.debug("Deployment created successfully ✓")
        except ApiException as e:
            if e.status == 409:
                logger.critical(f"Deployment already exists. Quitting..\n")
            elif e.status == 400:
                logger.critical(f"Invalid Deployment spec. Quitting..\n")
            else:
                logger.critical(f"Failed to create deployment. Error: {e}\nQuitting..\n")

            sys.exit(1)

    return


def main():
    app()
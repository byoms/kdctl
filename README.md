# kdctl
CLI tool to create and manage Kubernetes deployments

### Installation

#### Pre-requisites

  - Currently supported operating systems: GNU/Linux
  - [Install](https://docs.astral.sh/uv/getting-started/installation/) uv
  - Access to a Kubernetes cluster using a `kubeconfig` file

#### Steps

```sh
uv tool install --from git+https://github.com/byoms/kdctl kdctl
```

This installs the utility as a user local binary that can be invoked using `kdctl`. More details: [here](https://docs.astral.sh/uv/concepts/tools/#tool-executables)


## Usage

To **get started** & explore all the switches use `--help`

```sh
kdctl --help
```

### Creating a deployment

#### Understanding the premise or model

  - There are primarily 2 categories of users: Admins and Developers.
  - The _Developers_ belong to different teams within the organization are users of the Kubernetes platform.
  - The _Admins_ are part of a central team manage and operate the Kubernetes cluster infra, define governance policies.
  - Resources are isolated at a per-team level i.e each team is allocated a namespace. It operates within & has access access limited to that namespace.
  - The namespaces need to be created once per team - it is the responsibility of _Admins_ to facilitate this

#### Understanding the Deployment spec file

All application deployments need to be defined in a _deployment spec_ file. It is a yaml file expected in a particular structure.
 Here is a sample for ref.: [demo.yaml](docs/demo.yaml). It contains necessary details required for the deployment. Most fields are
 fairly self explanatory

#### kubeconfig

The tool uses the `kubeconfig` file to access the target Kubernetes cluster. There is an option to specify a custom path, if not it tries to use the default
 location: `$HOME/.kube/config`


### Example

Based on the above, lets consider a scenario. There is a new dev team named _devx_ and they have created an app named _txapp_ (using demo.yaml) that they want
 to run on Kubernetes. They are expected to first request the Admins to create a namespace for them and provide them with a kubeconfig file to access the cluster

```sh
kubectl create ns devx
```

After this, the dev team defines the deployment spec file and can create the deployment from CLI in the form of:  

```sh
kdctl create txapp.yaml --kubeconfig /path/to/user/kubeconfig
```

### Get deployment info

The tool also supports getting basic info of a deployment that is already created.

**Note assumption:** The current implementation assumes the name of the app that is deployed (the `name` field in deployment spec) as the unique identifier for
 a deployment for a given team - as it is highly unlikely to collide

The deployment info can be obtained for the above example using the team and app name

```sh
kdctl get devx txapp --kubeconfig /path/to/user/kubeconfig
```

---

## FUTURE SCOPE
  - Support horizontal pod autoscaling based on resource utilisation
  - Support autoscaling based on external systems using KEDA

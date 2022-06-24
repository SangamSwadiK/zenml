# 🔑 Managing Secrets with AWS/GCP Secret Manager

Most projects involving either cloud infrastructure or of a certain complexity
will involve secrets of some kind. A
ZenML Secret is a grouping of key-value pairs. These are accessed and
administered via the ZenML Secret Manager (a stack component).

## 🗺 Overview

The example pipeline is simple as can be. In our one and only step we access the
stacks active secret manager and
query for an example called `example_secret`. We then access the contents of
this secret and query the secret with the
unique key: `example_secret_key`.

Similarly, you would be able to pass access keys, password, credentials and so
on into your pipeline steps to do with as
you please.

# 🖥 Run it locally

## 👣 Step-by-Step

### 📄 Prerequisites

In order to run this example, you need to install and initialize ZenML. Within 
this example You'll be able to choose between using the
local yaml based secrets manager, 
the [AWS Secrets Manager](https://aws.amazon.com/secrets-manager/), 
the [GCP Secret Manager](https://cloud.google.com/secret-manager) or
the [Azure Key Vault](https://azure.microsoft.com/en-us/services/key-vault/#product-overview)

```shell
# install CLI
pip install zenml

# pull example
zenml example pull cloud_secrets_manager
cd zenml_examples/cloud_secrets_manager

# Initialize ZenML repo
zenml init
```

### 🥞 Set up your stack for AWS

To get going with aws make sure to have your aws credential set up locally. We
recommend this
[guide](https://docs.aws.amazon.com/sdk-for-java/v1/developer-guide/setup-credentials.html)
to make sure everything is
set up properly.

```shell
zenml integration install aws

zenml secrets-manager register aws_secrets_manager --flavor=aws
zenml stack register secrets_stack -m default -o default -a default -x aws_secrets_manager --set
```

### 🥞 Set up your stack for GCP

To get going with gcp make sure to have gcloud set up locally with a user or 
ideally a service account with permissions to access the secret manager. 
[This](https://cloud.google.com/sdk/docs/install-sdk) guide should help you get 
started. Once everything is set up on your machine, make sure to enable the 
secrets manager API within your GCP project. You will need to create a project
and get the `project_id` which will need to be specified when you register the
secrets manager.

```shell
zenml integration install gcp

zenml secrets-manager register gcp_secrets_manager --flavor=gcp_secrets_manager --project_id=PROJECT_ID
zenml stack register secrets_stack -m default -o default -a default -x gcp_secrets_manager --set
```

### 🥞 Set up your stack for Azure

To get going with Azure you will need to install and configure the 
[Azure CLI](https://docs.microsoft.com/en-us/cli/azure/install-azure-cli)
with the correct credentials to access the Azure secrets manager.

```shell
zenml integration install azure

zenml secrets-manager register azure_key_vault --flavor=azure_key_vault --key_vault_name=<VAULT-NAME>
zenml stack register secrets_stack -m default -o default -a default -x azure_key_vault --set
```

### Or stay on a local stack

In case you run into issues with either of the clouds, feel free to use a local 
secret manager. Just replace `--flavor=aws`/`--flavor=gcp_secrets_manager`/`--flavor=azure_key_vault`
with `--flavor=local` to use a file based version of a secret manager. Be aware that this is not 
a recommended location to store sensitive information.


### 🤫 Create a secret

Here we are creating a secret called `example_secret` which contains a single
key-value pair:
{example_secret_key: example_secret_value}

```shell
zenml secret register example_secret --example_secret_key=example_secret_value
```

### ▶️ Run the Code

Now we're ready. Execute:

```bash
python run.py
```

### 🧽 Clean up

In order to clean up, delete the example secret:

```shell
  zenml secret delete example_secret
```

and the remaining ZenML references.

```shell
rm -rf zenml_examples
```

# 📜 Learn more

If you want to learn more about secret managers in general or about how to build your own secret manager in ZenML
check out our [docs](https://docs.zenml.io/extending-zenml/secrets-manager).

We also have extensive CLI docs for the
[secret manager](https://apidocs.zenml.io/latest/cli/#zenml.cli--setting-up-a-secrets-manager)
and the
[secrets](https://apidocs.zenml.io/latest/cli/#zenml.cli--using-secrets).
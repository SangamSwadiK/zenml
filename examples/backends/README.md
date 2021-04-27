# Switching backends
One of the most powerful things in ZenML is the notion of backends. This is a showcase of different backends and how 
to use them together in various use-cases.

### Pre-requisites
In order to run this example, you need to clone the zenml repo.

```bash
git clone https://github.com/maiot-io/zenml.git
```

Before continuing, either [install the zenml pip package](https://docs.zenml.io/getting-started/installation.html) or
install it [from the cloned repo](../../zenml/README.md).

```
cd zenml
zenml init
cd examples/backends
```

You also need to enable the following GCP services (and enable billing).

* Google Compute VM
* Google Cloud AI Platform
* Google Cloud Storage
* Google Cloud Dataflow
* Google CloudSQL

### Run the project
Now we're ready. First fill in the env variables required. 

```bash
export GCP_BUCKET=""
export GCP_PROJECT=""
export GCP_REGION=""
export GCP_CLOUD_SQL_INSTANCE_NAME=""
export MODEL_NAME=""
export CORTEX_ENV=""
export MYSQL_DB=""
export MYSQL_USER=""
export MYSQL_PWD=""
export MYSQL_PORT=""
export MYSQL_HOST=""
```

Then run the jupyter notebook:

```bash
jupyter notebook
```

### Clean up
In order to clean up, in the root of your repo, delete the remaining zenml references.

```python
cd ../..
rm -r .zenml
rm -r pipelines
```

You can also delete your GCP project to clean up all resources associated with the pipeline runs.

## Caveats

## Next Steps
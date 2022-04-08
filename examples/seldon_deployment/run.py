#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
import click
from pipeline import (
    DeploymentTriggerConfig,
    SeldonDeployerConfig,
    SeldonDeploymentLoaderStepConfig,
    SklearnTrainerConfig,
    TensorflowTrainerConfig,
    continuous_deployment_pipeline_cache,
    deployment_trigger,
    dynamic_importer,
    importer_mnist,
    inference_pipeline,
    normalizer,
    prediction_service_loader,
    predictor,
    seldon_model_deployer,
    sklearn_evaluator,
    sklearn_predict_preprocessor,
    sklearn_trainer,
    tf_evaluator,
    tf_predict_preprocessor,
    tf_trainer,
)
from rich import print

from zenml.services import load_last_service_from_step


@click.command()
@click.option(
    "--deploy",
    "-d",
    is_flag=True,
    help="Run the deployment pipeline to train and deploy a model",
)
@click.option(
    "--predict",
    "-p",
    is_flag=True,
    help="Run the inference pipeline to send a prediction request "
    "to the deployed model",
)
@click.option(
    "--model-flavor",
    default="tensorflow",
    type=click.Choice(["tensorflow", "sklearn"]),
    help="Flavor of model being trained",
)
@click.option(
    "--epochs",
    default=7,
    help="Number of epochs for training (tensorflow hyperparam)",
)
@click.option(
    "--lr",
    default=0.002,
    help="Learning rate for training (tensorflow hyperparam, default: 0.003)",
)
@click.option(
    "--solver",
    default="saga",
    type=click.Choice(["newton-cg", "lbfgs", "liblinear", "sag", "saga"]),
    help="Algorithm to use in the optimization problem "
    "(sklearn hyperparam, default: saga)",
)
@click.option(
    "--penalty",
    default="l1",
    type=click.Choice(["l1", "l2", "elasticnet", "none"]),
    help="Regularization (penalty) norm (sklearn hyperparam, default: l1)",
)
@click.option(
    "--penalty-strength",
    default=1.0,
    type=float,
    help="Regularization (penalty) strength (sklearn hyperparam, default: 1.0)",
)
@click.option(
    "--toleration",
    default=0.1,
    type=float,
    help="Tolerance for stopping criteria (sklearn hyperparam, default: 0.1)",
)
@click.option(
    "--min-accuracy",
    default=0.92,
    help="Minimum accuracy required to deploy the model (default: 0.92)",
)
@click.option("--kubernetes-context", help="Kubernetes context to use.")
@click.option("--namespace", help="Kubernetes namespace to use.")
@click.option("--base-url", help="Seldon core ingress base URL.")
@click.option(
    "--stop-service",
    is_flag=True,
    default=False,
    help="Stop the prediction service when done",
)
def main(
    deploy: bool,
    predict: bool,
    model_flavor: str,
    epochs: int,
    lr: float,
    solver: str,
    penalty: str,
    penalty_strength: float,
    toleration: float,
    min_accuracy: float,
    kubernetes_context: str,
    namespace: str,
    base_url: str,
    stop_service: bool,
):
    """Run the Seldon example continuous deployment or inference pipeline

    Example usage:

    python run.py --deploy --predict \
        --model-flavor tensorflow \
        --kubernetes-context=zenml-eks-sandbox \
        --namespace=kubeflow \
        --base-url=http://abb84c444c7804aa98fc8c097896479d-377673393.us-east-1.elb.amazonaws.com \
        --min-accuracy 0.80
    """

    if stop_service:
        service = load_last_service_from_step(
            pipeline_name="continuous_deployment_pipeline",
            step_name="model_deployer",
            running=True,
        )
        if service:
            service.stop(timeout=100)
        return

    if model_flavor == "tensorflow":
        seldon_implementation = "TENSORFLOW_SERVER"
        trainer_config = TensorflowTrainerConfig(epochs=epochs, lr=lr)
        trainer = tf_trainer(trainer_config)
        evaluator = tf_evaluator()
        predict_preprocessor = tf_predict_preprocessor()
    else:
        seldon_implementation = "SKLEARN_SERVER"
        trainer_config = SklearnTrainerConfig(
            solver=solver,
            penalty=penalty,
            C=penalty_strength,
            tol=toleration,
        )
        trainer = sklearn_trainer(trainer_config)
        evaluator = sklearn_evaluator()
        predict_preprocessor = sklearn_predict_preprocessor()

    if deploy:
        # Initialize a continuous deployment pipeline run
        deployment = continuous_deployment_pipeline_cache(
            importer=importer_mnist(),
            normalizer=normalizer(),
            trainer=trainer,
            evaluator=evaluator,
            deployment_trigger=deployment_trigger(
                config=DeploymentTriggerConfig(
                    min_accuracy=min_accuracy,
                )
            ),
            model_deployer=seldon_model_deployer(
                config=SeldonDeployerConfig(
                    model_name="mnist",
                    step_name="model_deployer",
                    replicas=1,
                    implementation=seldon_implementation,
                    secret_name="seldon-rclone-secret",
                    kubernetes_context=kubernetes_context,
                    namespace=namespace,
                    base_url=base_url,
                    timeout=120,
                    parameters=[{"name": "method", "type": "STRING", "value": "predict_proba"},],
                )
            ),
        )

        deployment.run()

    if predict:
        # Initialize an inference pipeline run
        inference = inference_pipeline(
            dynamic_importer=dynamic_importer(),
            predict_preprocessor=predict_preprocessor,
            prediction_service_loader=prediction_service_loader(
                SeldonDeploymentLoaderStepConfig(
                    pipeline_name="continuous_deployment_pipeline_cache",
                    step_name="model_deployer",
                )
            ),
            predictor=predictor(),
        )

        inference.run()

    try:
        service = load_last_service_from_step(
            pipeline_name="continuous_deployment_pipeline_cache",
            step_name="model_deployer",
            running=True,
        )
        print(
            f"The Seldon prediction server is running remotely as a Kubernetes "
            f"service and accepts inference requests at:\n"
            f"    {service.prediction_url}\n"
            f"To stop the service, re-run the same command and supply the "
            f"`--stop-service` argument."
        )
    except KeyError:
        print(
            "No Seldon prediction server is currently running. The deployment "
            "pipeline must run first to train a model and deploy it. Execute "
            "the same command with the `--deploy` argument to deploy a model."
        )


if __name__ == "__main__":
    main()
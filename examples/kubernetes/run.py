from pipelines.training_pipeline import training_pipeline
from steps import (
    deployment_trigger,
    evaluator,
    skew_comparison,
    svc_trainer_mlflow,
    training_data_loader,
)

from zenml.integrations.mlflow.steps import mlflow_model_deployer_step

if __name__ == "__main__":
    training_pipeline(
        training_data_loader=training_data_loader(),
        skew_comparison=skew_comparison(),
        trainer=svc_trainer_mlflow(),
        evaluator=evaluator(),
        deployment_trigger=deployment_trigger(),
        model_deployer=mlflow_model_deployer_step(),
    ).run()

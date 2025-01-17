#  Copyright (c) ZenML GmbH 2022. All Rights Reserved.
#
#  Licensed under the Apache License, Version 2.0 (the "License");
#  you may not use this file except in compliance with the License.
#  You may obtain a copy of the License at:
#
#       https://www.apache.org/licenses/LICENSE-2.0
#
#  Unless required by applicable law or agreed to in writing, software
#  distributed under the License is distributed on an "AS IS" BASIS,
#  WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
#  or implied. See the License for the specific language governing
#  permissions and limitations under the License.
"""Step that allows you to post messages to Slack."""

from zenml.alerter.alerter_utils import get_active_alerter
from zenml.integrations.slack.alerters.slack_alerter import (
    SlackAlerter,
    SlackAlerterConfig,
)
from zenml.steps import StepContext, step


@step
def slack_alerter_post_step(
    config: SlackAlerterConfig, context: StepContext, message: str
) -> bool:
    """Post a message to the Slack alerter component of the active stack.

    Args:
        config: Runtime configuration for the Slack alerter.
        context: StepContext of the ZenML repository.
        message: Message to be posted.

    Returns:
        True if operation succeeded, else False.

    Raises:
        RuntimeError: If currently active alerter is not a `SlackAlerter`.
    """
    alerter = get_active_alerter(context)
    if not isinstance(alerter, SlackAlerter):
        raise RuntimeError(
            "Step `slack_alerter_post_step` requires an alerter component of "
            "flavor `slack`, but the currently active alerter is of type "
            f"{type(alerter)}, which is not a subclass of `SlackAlerter`."
        )
    return alerter.post(message, config)

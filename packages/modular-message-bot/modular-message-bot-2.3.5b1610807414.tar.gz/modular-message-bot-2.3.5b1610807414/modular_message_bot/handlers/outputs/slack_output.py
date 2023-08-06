import logging

import requests

from modular_message_bot.handlers.outputs.abstract_output_hander import AbstractSimpleOutputHandler
from modular_message_bot.models.job import JobConfigSection

logger = logging.getLogger(__name__)


class SlackOutput(AbstractSimpleOutputHandler):
    @classmethod
    def get_code(cls) -> str:
        return "slack"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' output"

        # Required parameters
        for required_param_key in ["payload", "url"]:
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}"

        # Required parameters.payload
        for required_param_arg_key in ["text"]:
            if required_param_arg_key not in parameters["payload"].keys():
                return f"payload.'{required_param_arg_key}' {message_suffix}"

        return super().validate_job_config(job_config)

    def run_output(self, parameters: dict):
        logger.info("Slack: Sending message")

        url = parameters.get("url")
        payload = parameters.get("payload")

        result = requests.post(url, json=payload)

        logger.info(f"Slack: Send Result - status:'{result.status_code}'")
        if str(result.status_code) != "200":
            raise Exception(f"ERROR: Response from request was {result.status_code}\n{result.content}")

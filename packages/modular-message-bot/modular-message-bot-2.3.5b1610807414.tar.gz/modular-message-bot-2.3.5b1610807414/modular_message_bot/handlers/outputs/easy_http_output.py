import logging

import requests

from modular_message_bot.handlers.outputs.abstract_output_hander import AbstractSimpleOutputHandler
from modular_message_bot.models.job import JobConfigSection

logger = logging.getLogger(__name__)


class EasyHttpOutput(AbstractSimpleOutputHandler):
    @classmethod
    def get_code(cls) -> str:
        return "easy_http"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' output"

        # Required parameters
        for required_param_key in ["url"]:
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}"

        return super().validate_job_config(job_config)

    def run_output(self, parameters: dict):
        # Settings
        url = parameters.get("url")
        method = parameters.get("method", "post")
        ignore_failure = parameters.get("ignore-failure", False)
        args = parameters.get("args", {})
        log_details = f"{self.get_code()} url: '{url}'\n method: '{method}'\n ignore_failure: '{ignore_failure}'"
        logger.debug(log_details)

        result = requests.request(method, url, **args)
        logger.debug(f"Response for {self.get_code()} was {result.status_code}\n{result.content}")

        if str(result.status_code) != "200":
            logger.warning(f"Request to failed! {log_details}")
            if not ignore_failure:
                raise Exception(f"ERROR: Response failure {result.status_code}\n{result.content}")

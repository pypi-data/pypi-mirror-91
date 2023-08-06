import logging

from requests import post as request_post

from modular_message_bot.handlers.outputs.abstract_output_hander import AbstractSimpleOutputHandler
from modular_message_bot.models.job import JobConfigSection

logger = logging.getLogger(__name__)


class PushoverOutput(AbstractSimpleOutputHandler):
    send_url = "https://api.pushover.net/1/messages.json"
    validation_url = "https://api.pushover.net/1/users/validate.json"
    docs_link = "https://pushover.net/api"
    required_parameter_keys = ["token", "user", "message"]
    optional_parameter_keys = [
        # "attachment",
        "device",
        "title",
        "url",
        "url_title",
        "priority",
        "sound",
        "timestamp",
    ]

    @classmethod
    def get_code(cls) -> str:
        return "pushover"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' output. Please see {self.docs_link}"
        for required_param_key in self.required_parameter_keys:
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}"
        # url_validation = self.url_validate_parameters(parameters)
        # if url_validation != "":
        #     return url_validation
        return super().validate_job_config(job_config)

    # This requires the parameters to be interpolated to work
    # See: https://gitlab.com/mage-sauce/programs/modular-message-bot/-/issues/6
    # def url_validate_parameters(self, parameters: dict) -> str:
    #     """
    #     Validates the parameters against the pushover api
    #     See: https://pushover.net/api#validate
    #     :param parameters: dict
    #     :return: str
    #     """
    #     headers = {"Content-Type": "application/json"}
    #     send = self.get_send_parameters(parameters)
    #     result = requests.post(self.validation_url, headers=headers, json=send)
    #     result_json = result.json()
    #     if str(result.status_code) != "200":
    #         return "".join(result_json.get("errors", ""))
    #     return ""

    def get_send_parameters(self, parameters: dict):
        send = {}
        for required_parameter_key in self.required_parameter_keys:
            send[required_parameter_key] = parameters.get(required_parameter_key)
        for optional_parameter_key in self.optional_parameter_keys:
            if optional_parameter_key in parameters.keys():
                send[optional_parameter_key] = parameters[optional_parameter_key]
        return send

    def run_output(self, parameters: dict):
        # Settings
        send = self.get_send_parameters(parameters)
        headers = {"Content-Type": "application/json"}
        logger.info("Sending pushover request")
        result = request_post(self.send_url, headers=headers, json=send)

        if str(result.status_code) != "200":
            raise Exception(f"ERROR: Response failure {result.status_code}\n{result.content}")

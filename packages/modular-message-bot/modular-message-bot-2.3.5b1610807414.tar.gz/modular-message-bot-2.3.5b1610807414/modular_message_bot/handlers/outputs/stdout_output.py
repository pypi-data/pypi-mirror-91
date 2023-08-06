from modular_message_bot.handlers.outputs.abstract_output_hander import AbstractSimpleOutputHandler
from modular_message_bot.models.job import JobConfigSection
from modular_message_bot.utils.common_utils import write_to_standard_out


class StdoutOutput(AbstractSimpleOutputHandler):
    @classmethod
    def get_code(cls) -> str:
        return "stdout"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' output"

        # Required parameters
        for required_param_key in ["message"]:
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}"

        return super().validate_job_config(job_config)

    def run_output(self, parameters: dict):
        # Settings
        write_to_standard_out(parameters.get("message"))

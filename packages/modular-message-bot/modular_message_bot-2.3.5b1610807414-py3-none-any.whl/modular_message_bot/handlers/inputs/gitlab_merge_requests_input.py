import logging
from urllib.parse import urlencode

import jq
from requests import get as requests_get

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job_run import JobRunVarCollection

logger = logging.getLogger(__name__)


class GitlabMergeRequestsInput(AbstractSimpleInputHandler):
    url = "https://gitlab.com/api"

    @classmethod
    def get_code(cls) -> str:
        return "gitlab_merge_requests"

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        url_prefix = parameters.get("url", self.url)
        get_params = parameters.get("get", {"state": "opened"})
        request_args = parameters.get("request-args", {})
        jq_vars = parameters.get("jq-vars", {})
        jq_var_join = parameters.get("jq-var-join", "")
        project_ids = parameters.get("project-ids", [])

        # Loop repos and have a look for open PRs
        responses = []
        for project_id in project_ids:
            url = f"{url_prefix}/v4/projects/{project_id}/merge_requests?{urlencode(get_params)}"
            response = requests_get(url, **request_args)
            if response.status_code != 200:
                raise Exception(f"{self.get_code()} failed '{response.status_code}'\n'{response.content}'")
            responses += response.json()
        logger.debug(f"{self.get_code()} found {len(responses)} total responses")

        # Filter data (JQ)
        for var, jq_query in jq_vars.items():
            jq_results = jq.compile(jq_query).input(responses).all()
            joined_result = jq_var_join.join(map(str, jq_results))
            value = str(joined_result).strip('"')
            job_run_vars_collection.interpolate(var, value, self.get_code())

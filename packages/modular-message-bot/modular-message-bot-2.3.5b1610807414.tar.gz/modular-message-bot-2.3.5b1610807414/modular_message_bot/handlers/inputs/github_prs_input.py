import logging
from urllib.parse import urlencode

import jq
from requests import get as requests_get
from requests.auth import HTTPBasicAuth

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job_run import JobRunVarCollection

logger = logging.getLogger(__name__)


class GithubPrsInput(AbstractSimpleInputHandler):
    url = "https://api.github.com"

    @classmethod
    def get_code(cls) -> str:
        return "github_prs"

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        url_prefix = parameters.get("url", self.url)
        get_params = parameters.get("get", {"state": "open"})
        jq_vars = parameters.get("jq-vars", {})
        jq_var_join = parameters.get("jq-var-join", "")
        auth_user = parameters.get("auth-user", "")
        auth_token = parameters.get("auth-token", "")
        repos = parameters.get("repos", [])
        headers = parameters.get("headers", {})

        # Loop repos and have a look for open PRs
        responses = []
        headers["Accept"] = "application/vnd.github.v3+json"
        args = {"headers": headers}
        if auth_user != "" or auth_token != "":
            args["auth"] = HTTPBasicAuth(auth_user, auth_token)
        for repo in repos:
            url = f"{url_prefix}/repos/{repo}/pulls?{urlencode(get_params)}"
            response = requests_get(url, **args)
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

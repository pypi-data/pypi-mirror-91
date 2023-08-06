import jq
from elasticsearch import Elasticsearch

from modular_message_bot.handlers.inputs.abstract_input_handler import AbstractSimpleInputHandler
from modular_message_bot.models.job import JobConfigSection
from modular_message_bot.models.job_run import JobRunVarCollection


class ElasticSearchInput(AbstractSimpleInputHandler):
    # https://github.com/elastic/examples/tree/master/Miscellaneous/docker/full_stack_example
    docs_search_param = (
        "https://elasticsearch-py.readthedocs.io/en/7.10.0/api.html?highlight=search"
        "#elasticsearch.Elasticsearch.search"
    )

    @classmethod
    def get_code(cls) -> str:
        return "elasticsearch"

    def validate_job_config(self, job_config: JobConfigSection) -> str:
        parameters = job_config.parameters
        message_suffix = f"is required for '{self.get_code()}' input"

        required_param_keys = {"search": f". See {self.docs_search_param}"}

        # Required parameters
        for required_param_key, additional_details in required_param_keys.items():
            if required_param_key not in parameters.keys():
                return f"'{required_param_key}' {message_suffix}{additional_details}"

        return super().validate_job_config(job_config)

    def run_input(self, parameters: dict, job_run_vars_collection: JobRunVarCollection):
        connection: dict = parameters.get("connection", {})
        search: dict = parameters["search"]
        jq_vars: dict = parameters.get("jq-vars", {})
        jq_var_join: str = parameters.get("jq-var-join", "")

        es = Elasticsearch(**connection)
        es_results = es.search(**search)

        # Filter data (JQ)
        for var, jq_query in jq_vars.items():
            jq_results = jq.compile(jq_query).input(es_results).all()
            joined_result = jq_var_join.join(map(str, jq_results))
            value = str(joined_result)
            job_run_vars_collection.interpolate(var, value, self.get_code())

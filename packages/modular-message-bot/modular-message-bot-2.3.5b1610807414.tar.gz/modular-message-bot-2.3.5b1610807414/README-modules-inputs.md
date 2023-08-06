# Input Modules
Modules that grab inputs from somewhere

## Patterns

### jq-vars
jq-vars is a dict, with the key being the var to replace `{var}` in the `vars:` job definition. The value is a JQ
expression. With this we can extract parts of a external response without multiple calls.
See: https://stedolan.github.io/jq/
Have a look in `tests/component-resources/job-*.yml` for examples. You can also test your queries using test data.
For example `cat tests/component-resources/response-open-weather-city.json | jq "\"Test: \" + .weather[0].description"`
Note: YQ also exists for YML/YAML responses if you want to call an API yourself. See: `https://pypi.org/project/yq/`

## Specifics

### Datetime Input Module
This is a wrapper for Python Date. Format options come from Python date function

Example Simple Input:
```yaml
- code: datetime
  parameters:
    var: date
    format: '%c'
```

Example Advanced Input:
```yaml
- code: datetime
  parameters:
    var: date
    format: '%c'
    # Add some time (see timedelta in https://docs.python.org/3/library/datetime.html)
    add:
       hours: 1
       minutes: 10
    # Subtract some time (see timedelta in https://docs.python.org/3/library/datetime.html)
    sub:
       days: 2
       seconds: 50
```

### Elastic Search Input Module
You can query Elastic Search and preform a search query. This is a wrapper around 
https://elasticsearch-py.readthedocs.io/en/7.10.0/api.html?highlight=search#elasticsearch.Elasticsearch.search
For example you could push the output to Slack

jq-vars test:
`cat tests/component-resources/response-elasticsearch.json | jq -r ". | .hits.hits | map([._source.\"@timestamp\", ._source.docker.message] | join(\" - \")) | join(\"\n\")"`

Example Input:
```yaml
- code: elasticsearch
  parameters:
    connection:
      hosts:
        - host: "testelk"
          port: 9200
      http_auth:
        - "elastic"
        - "changeme"
    search:
      index: "docker-logs-*"
      q: "docker.message: error AND NOT docker.container_id: 81f0bb3014f1"
    jq-vars:
      number: ". | .hits.hits | length"
      details: ". | .hits.hits | map([._source.\"@timestamp\", ._source.docker.message] | join(\" - \")) | join(\"\n\")"
```

### Github PR Input Module
Calls Github looking for Pulls (PRs) for a list of repositories
This is a wrapper around https://docs.github.com/en/free-pro-team@latest/rest/reference/pulls

jq-vars test:
`cat tests/component-resources/response-github-pr-jeremy-test-org-2---test-repo-2a.json | jq -r ". | map([.html_url] | join(\"\")) | join(\"\n\")"`

Example Simple Input:
```yaml
- code: github_prs
  parameters:
    auth-user: $[GITHUB_COM_USERNAME]
    auth-token: $[GITHUB_COM_TOKEN]
    repos:
      - group-name/repository-one
      - group-name/repository-two
      - group-name/repository-three
      - group-name/repository-four
    jq-vars:
      pr_details: ". | map([.html_url] | join(\"\")) | join(\"\n\")"
```

Example Advanced Input:
```yaml
- code: github_prs
  parameters:
    auth-user: $[GITHUB_COM_USERNAME]
    auth-token: $[GITHUB_COM_TOKEN]
    repos:
      - jeremy-test-org-1/test-repo-1a
      - jeremy-test-org-1/test-repo-1b
      - jeremy-test-org-2/test-repo-2a
      - jeremy-test-org-2/test-repo-2b
    get:
      state: open
    headers:
       Something: Else
    jq-vars:
      pr_count: "length"
      pr_details: ". | map([.head.repo.full_name, \" - \", .title, \" - by \", .user.login, \" - \", .html_url] | join(\"\")) | join(\"\n\")"
    jq-var-join: ""
```

## Gitlab Pull Requests Input Module
Calls Gitlab looking for merge requests for a list of projects
This is a wrapper around https://docs.gitlab.com/ee/api/merge_requests.html#list-project-merge-requests

jq-vars test:
`cat tests/component-resources/response-gitlab-merge-requests-23648575.json | jq -r ". | map([.web_url] | join(\"\")) | join(\"\n\")"`

Example Simple Input:
```yaml
- code: gitlab_merge_requests
  parameters:
    project-ids:
      - 23648646 # public - 0 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-0
      - 23648520 # public - 1 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-1
      - 23648575 # public - 2 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-2
    request-args:
      headers:
        PRIVATE-TOKEN: "$[GITLAB_TOKEN]"
    jq-vars:
      pr_count: "length"
      pr_details: ". | map([.web_url] | join(\"\")) | join(\"\n\")"
```

Example Advanced Input:
```yaml
- code: gitlab_merge_requests
  parameters:
    url: https://gitlab.example.com/api
    project-ids:
      - 23648646 # public - 0 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-0
      - 23648520 # public - 1 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-1
      - 23648575 # public - 2 pr(s) - https://gitlab.com/mage-sauce/tests/test-merge-requests-2
    get:
      state: opened
    request-args:
      headers:
        PRIVATE-TOKEN: "$[GITLAB_TOKEN]"
    jq-vars:
      pr_count: "length"
      pr_details: ". | map([.references.full, \" - \", .title, \" - by \", .author.name, \" - \", .web_url] | join(\"\")) | join(\"\n\")"
    jq-var-join: ""
```


### Open Weather City Input Module
Please read the LICENSE for OpenWeatherMap carefully, it is your responsibility!
Get an API key at https://home.openweathermap.org/users/sign_up

jq-vars test:
`cat tests/component-resources/response-open-weather-city.json | jq "\"Test: \" + .weather[0].description"`

Example Input:
```yaml
- code: open_weather_city
  parameters:
    query:
      q: edinburgh,uk
      appid: "$[OPEN_WEATHER_KEY]"
    jq-vars:
      weather_msg: ".slack_icon + \" \" + .weather[0].description + \" \" + .weather_by_with_link"
      another_msg: ".weather[0].description + \" \" + .weather_by"
```
In the example above, two vars will be created `weather_msg` and `another_msg`

### Random Message Input Module
This takes random vars and adds them to another var
i.e. Take all job vars with a code prefix of "x" and add a random one to var "y"

```yaml
- code: random_message
  parameters:
     match:
        x: "^y"
```
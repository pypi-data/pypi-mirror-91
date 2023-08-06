#!/usr/bin/env bash

set -e

# This is a development script
# It queries a list of Gitlab repos for open merge requests and saves the results for use in tests

source .env

PROJECT_IDS=(
  "23648646" # https://gitlab.com/mage-sauce/tests/test-merge-requests-0
  "23648520" # https://gitlab.com/mage-sauce/tests/test-merge-requests-1
  "23648575" # https://gitlab.com/mage-sauce/tests/test-merge-requests-2
)

for PROJECT_ID in "${PROJECT_IDS[@]}"; do

  # Curl Github and download the test data
  curl --header "PRIVATE-TOKEN: ${GITLAB_COM_TOKEN}" \
    "https://gitlab.com/api/v4/projects/${PROJECT_ID}/merge_requests?state=opened" \
    > tests/component-resources/response-gitlab-merge-requests-${PROJECT_ID}.json

  # Place the result in the component-resources and unit-resources directories
  cp  tests/component-resources/response-gitlab-merge-requests-${PROJECT_ID}.json \
      tests/unit-resources/response-gitlab-merge-requests-${PROJECT_ID}.json
done


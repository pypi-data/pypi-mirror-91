#!/usr/bin/env bash

set -e

# This is a development script
# It queries a list of Github repos for open pull requests and saves the results for use in tests

source .env

REPOS=(
  "jeremy-test-org-1/test-repo-1a"
  "jeremy-test-org-1/test-repo-1b"
  "jeremy-test-org-2/test-repo-2a"
  "jeremy-test-org-2/test-repo-2b"
)

for REPO in "${REPOS[@]}"; do
  # Replace the "/" with "---"
  OUTPUT_CODE="${REPO//\//---}"

  # Curl Github and download the test data
  curl -u ${GITHUB_COM_USERNAME}:${GITHUB_COM_TOKEN} \
    "https://api.github.com/repos/${REPO}/pulls?state=open" \
    > tests/component-resources/response-github-pr-${OUTPUT_CODE}.json

  # Place the result in the component-resources and unit-resources directories
  cp  tests/component-resources/response-github-pr-${OUTPUT_CODE}.json \
      tests/unit-resources/response-github-pr-${OUTPUT_CODE}.json
done


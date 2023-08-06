from unittest.mock import MagicMock, Mock, call

from modular_message_bot.run_by_id import run

from tests.component.conftest import TestingConfigProvider, get_test_data, get_test_data_json, get_test_data_yaml


def test_stdout(
    mock_get_run_details: MagicMock, mock_stdout_output_write_to_standard_out: MagicMock,
):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-stdout.yml")

    # When
    run("bae50216-ae35-45c6-b9e3-45c305ae770e")

    # Then
    mock_stdout_output_write_to_standard_out.assert_called_once_with("Hello World!")


def test_stdout_interpolated(
    mock_get_run_details: MagicMock,
    mock_stdout_output_write_to_standard_out: MagicMock,
    testing_config: TestingConfigProvider,
):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-stdout-interpolated.yml")
    testing_config.add("FIRST", "HELLO")
    testing_config.add("SECOND", "World!!")

    # When
    run("ad7e2bc2-6626-4526-b89b-312cef2ea079")

    # Then
    mock_stdout_output_write_to_standard_out.assert_called_once_with("HELLO World!!!")


def test_stdout_message(
    mock_get_run_details: MagicMock, mock_stdout_output_write_to_standard_out: MagicMock,
):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-stdout-message.yml")

    # When
    run("fdc762d2-eab6-4440-bf43-d12344d20246")

    # Then
    mock_stdout_output_write_to_standard_out.assert_called_once_with("Hello World!!")


def test_stdout_message_interpolated(
    mock_get_run_details: MagicMock,
    mock_stdout_output_write_to_standard_out: MagicMock,
    testing_config: TestingConfigProvider,
):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-stdout-message-interpolated.yml")
    testing_config.add("FIRST", "Hello")
    testing_config.add("SECOND", "World")
    testing_config.add("THIRD", "!!!!!")

    # When
    run("2c981856-81b8-4f62-b355-29ca60aa1756")

    # Then
    mock_stdout_output_write_to_standard_out.assert_called_once_with("Hello World !!!!!")


def test_stdout_datetime(
    mock_get_run_details: MagicMock, mock_stdout_output_write_to_standard_out: MagicMock,
):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-stdout-datetime.yml")

    # When
    run("b1e5b926-242f-4f4a-a0d8-426141b0743d")

    # Then
    mock_stdout_output_write_to_standard_out.assert_called_once_with(
        "Hello World!!! It's Week 52 (day 364) - Tuesday December 29/12/20"
    )


def test_stdout_datetime_shifted(
    mock_get_run_details: MagicMock, mock_stdout_output_write_to_standard_out: MagicMock,
):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-stdout-datetime-shifted.yml")

    # When
    run("c20b1590-0be8-4cc6-845b-72eef3019c1c")

    # Then
    mock_stdout_output_write_to_standard_out.assert_called_once_with("Hello. It's Sun 27 Dec 2020 21:00:28 UTC")


def test_stdout_weather(
    testing_config: TestingConfigProvider,
    mock_get_run_details: MagicMock,
    mock_open_weather_city_input_requests: MagicMock,
    mock_stdout_output_write_to_standard_out: MagicMock,
):
    # Given
    testing_config.add("OPEN_WEATHER_KEY", "a1b2c3")
    mock_get_run_details.return_value = get_test_data_yaml("job-stdout-weather.yml")
    mock_open_weather_city_input_requests_get = MagicMock()
    mock_open_weather_city_input_requests_get.status_code = 200
    mock_open_weather_city_input_requests_get.json.return_value = get_test_data_json("response-open-weather-city.json")
    mock_open_weather_city_input_requests.get.return_value = mock_open_weather_city_input_requests_get

    # When
    run("d36d6785-0013-4e6c-90e9-9ebd49047a4b")

    # Then
    mock_stdout_output_write_to_standard_out.assert_called_once_with(
        "Edi weather is broken clouds Weather by Openweathermap\n"
        "Edinburgh weather is :cloud: broken clouds Weather by Openweathermap (openweathermap.org)"
    )
    mock_open_weather_city_input_requests.get.assert_called_once_with(
        "https://api.openweathermap.org/data/2.5/weather", params={"q": "edinburgh,uk", "appid": "a1b2c3"},
    )


def test_slack_datetime(
    mock_get_run_details: MagicMock, mock_slack_output_requests: MagicMock, testing_config: TestingConfigProvider,
):
    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    testing_config.add("SLACK_NAME", "autobot")
    mock_get_run_details.return_value = get_test_data_yaml("job-slack-datetime.yml")
    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    # When
    run("843a1372-d4b7-4744-bb28-535ad356e6ee")

    # Then
    mock_slack_output_requests.post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXX",
        json={
            "text": "It's currently Tue 29 Dec 2020 19:51:18 UTC\nHope you are having a good day",
            "channel": "#test",
            "post-as": "autobot",
            "icon_emoji": ":information_source:",
        },
    )


def test_slack_github_open_prs(
    mock_get_run_details: MagicMock,
    mock_github_prs_input_requests_get: MagicMock,
    mock_github_prs_input_http_basic_auth: MagicMock,
    mock_slack_output_requests: MagicMock,
    testing_config: TestingConfigProvider,
):
    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    testing_config.add("SLACK_NAME", "autobot")
    testing_config.add("GITHUB_COM_USERNAME", "somebody")
    testing_config.add("GITHUB_COM_TOKEN", "a1b2c3d4e5f6g7")
    mock_get_run_details.return_value = get_test_data_yaml("job-slack-github-open-prs.yml")
    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    mock_response1 = Mock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-1---test-repo-1a.json")

    mock_response2 = Mock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-1---test-repo-1b.json")

    mock_response3 = Mock()
    mock_response3.status_code = 200
    mock_response3.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-2---test-repo-2a.json")

    mock_response4 = Mock()
    mock_response4.status_code = 200
    mock_response4.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-2---test-repo-2b.json")

    mock_github_prs_input_requests_get.side_effect = [mock_response1, mock_response2, mock_response3, mock_response4]

    # When
    run("ce85dda5-5735-420e-a3ec-307e2433e9fb")

    # Then
    expected_pr_details = (
        "jeremy-test-org-1/test-repo-1a"
        " - Update README.md"
        " - by jeremysells"
        " - https://github.com/jeremy-test-org-1/test-repo-1a/pull/1"
        "\n"
        "jeremy-test-org-2/test-repo-2a"
        " - Something something readme something"
        " - by jeremysells"
        " - https://github.com/jeremy-test-org-2/test-repo-2a/pull/2"
        "\n"
        "jeremy-test-org-2/test-repo-2a"
        " - Update README.md blah blah"
        " - by jeremysells"
        " - https://github.com/jeremy-test-org-2/test-repo-2a/pull/1"
    )
    mock_slack_output_requests.post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXX",
        json={
            "text": f"Tue 29 Dec 2020 19:51:18 UTC - you have 3 open PR(s).\n{expected_pr_details}",
            "channel": "#test",
            "username": "autobot",
            "icon_emoji": ":robot_face:",
        },
    )
    mock_github_prs_input_http_basic_auth.assert_called_once_with("somebody", "a1b2c3d4e5f6g7")
    mock_github_prs_input_requests_get.assert_has_calls(
        [
            call(
                "https://example-api.github.com/repos/jeremy-test-org-1/test-repo-1a/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_github_prs_input_http_basic_auth.return_value,
            ),
            call(
                "https://example-api.github.com/repos/jeremy-test-org-1/test-repo-1b/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_github_prs_input_http_basic_auth.return_value,
            ),
            call(
                "https://example-api.github.com/repos/jeremy-test-org-2/test-repo-2a/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_github_prs_input_http_basic_auth.return_value,
            ),
            call(
                "https://example-api.github.com/repos/jeremy-test-org-2/test-repo-2b/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_github_prs_input_http_basic_auth.return_value,
            ),
        ]
    )


def test_slack_github_open_prs_none(
    mock_get_run_details: MagicMock,
    mock_github_prs_input_requests_get: MagicMock,
    mock_github_prs_input_http_basic_auth: MagicMock,
    mock_slack_output_requests: MagicMock,
    testing_config: TestingConfigProvider,
):
    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    testing_config.add("SLACK_NAME", "autobot")
    testing_config.add("GITHUB_COM_USERNAME", "somebody")
    testing_config.add("GITHUB_COM_TOKEN", "a1b2c3d4e5f6g7")
    mock_get_run_details.return_value = get_test_data_yaml("job-slack-github-open-prs-none.yml")
    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    mock_response1 = Mock()
    mock_response1.status_code = 200
    mock_response1.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-1---test-repo-1b.json")

    mock_response2 = Mock()
    mock_response2.status_code = 200
    mock_response2.json.return_value = get_test_data_json("response-github-pr-jeremy-test-org-2---test-repo-2b.json")

    mock_github_prs_input_requests_get.side_effect = [mock_response1, mock_response2]

    # When
    run("ce85dda5-5735-420e-a3ec-307e2433e9fb")

    # Then
    mock_slack_output_requests.post.assert_not_called()
    mock_github_prs_input_http_basic_auth.assert_called_once_with("somebody", "a1b2c3d4e5f6g7")
    mock_github_prs_input_requests_get.assert_has_calls(
        [
            call(
                "https://api.github.com/repos/jeremy-test-org-1/test-repo-1b/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_github_prs_input_http_basic_auth.return_value,
            ),
            call(
                "https://api.github.com/repos/jeremy-test-org-2/test-repo-2b/pulls?state=open",
                headers={"Accept": "application/vnd.github.v3+json"},
                auth=mock_github_prs_input_http_basic_auth.return_value,
            ),
        ]
    )


def test_slack_gitlab_open_merge_requests(
    mock_get_run_details: MagicMock,
    mock_gitlab_merge_requests_input_requests_get: MagicMock,
    mock_slack_output_requests: MagicMock,
    testing_config: TestingConfigProvider,
):
    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    testing_config.add("SLACK_NAME", "autobot")
    testing_config.add("GITLAB_TOKEN", "a1b2c3d4e5f6g7")
    mock_get_run_details.return_value = get_test_data_yaml("job-slack-gitlab-open-merge-requests.yml")
    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    response_files = [
        "response-gitlab-merge-requests-23648646.json",
        "response-gitlab-merge-requests-23648520.json",
        "response-gitlab-merge-requests-23648575.json",
    ]
    mock_calls = []
    for response_file in response_files:
        mock_call = Mock()
        mock_call.status_code = 200
        mock_call.json.return_value = get_test_data_json(response_file)
        mock_calls.append(mock_call)
    mock_gitlab_merge_requests_input_requests_get.side_effect = mock_calls

    # When
    run("bb215ff9-6f43-445c-839b-1e1034324d1d")

    # Then
    expected_pr_details = (
        "mage-sauce/tests/test-merge-requests-1!1"
        " - Test merge request 1a"
        " - by Jeremy Sells"
        " - https://gitlab.com/mage-sauce/tests/test-merge-requests-1/-/merge_requests/1"
        "\n"
        "mage-sauce/tests/test-merge-requests-2!2"
        " - Test merge request 2b"
        " - by Jeremy Sells"
        " - https://gitlab.com/mage-sauce/tests/test-merge-requests-2/-/merge_requests/2"
        "\n"
        "mage-sauce/tests/test-merge-requests-2!1"
        " - Test merge request 2a"
        " - by Jeremy Sells"
        " - https://gitlab.com/mage-sauce/tests/test-merge-requests-2/-/merge_requests/1"
    )
    mock_slack_output_requests.post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXX",
        json={
            "text": f"Tue 29 Dec 2020 19:51:18 UTC - you have 3 open Merge Requests(s).\n{expected_pr_details}",
            "channel": "#test",
            "username": "autobot",
            "icon_emoji": ":robot_face:",
        },
    )
    mock_gitlab_merge_requests_input_requests_get.assert_has_calls(
        [
            call(
                "https://gitlab.com/api/v4/projects/23648646/merge_requests?state=opened",
                headers={"PRIVATE-TOKEN": "a1b2c3d4e5f6g7"},
            ),
            call(
                "https://gitlab.com/api/v4/projects/23648520/merge_requests?state=opened",
                headers={"PRIVATE-TOKEN": "a1b2c3d4e5f6g7"},
            ),
            call(
                "https://gitlab.com/api/v4/projects/23648575/merge_requests?state=opened",
                headers={"PRIVATE-TOKEN": "a1b2c3d4e5f6g7"},
            ),
        ]
    )


def test_slack_gitlab_open_merge_requests_none(
    mock_get_run_details: MagicMock,
    mock_gitlab_merge_requests_input_requests_get: MagicMock,
    mock_slack_output_requests: MagicMock,
    testing_config: TestingConfigProvider,
):
    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    testing_config.add("SLACK_NAME", "autobot")
    testing_config.add("GITLAB_TOKEN", "a1b2c3d4e5f6g7")
    mock_get_run_details.return_value = get_test_data_yaml("job-slack-gitlab-open-merge-requests-none.yml")
    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    response_files = [
        "response-gitlab-merge-requests-23648646.json",
        "response-gitlab-merge-requests-23648646.json",
    ]
    mock_calls = []
    for response_file in response_files:
        mock_call = Mock()
        mock_call.status_code = 200
        mock_call.json.return_value = get_test_data_json(response_file)
        mock_calls.append(mock_call)
    mock_gitlab_merge_requests_input_requests_get.side_effect = mock_calls

    # When
    run("45047c2b-1f9d-4e75-b999-647afebd1cba")

    # Then
    mock_slack_output_requests.post.assert_not_called()
    mock_gitlab_merge_requests_input_requests_get.assert_has_calls(
        [
            call(
                "https://gitlab.com/api/v4/projects/23648646/merge_requests?state=opened",
                headers={"PRIVATE-TOKEN": "a1b2c3d4e5f6g7"},
            ),
            call(
                "https://gitlab.com/api/v4/projects/23648646/merge_requests?state=opened",
                headers={"PRIVATE-TOKEN": "a1b2c3d4e5f6g7"},
            ),
        ]
    )


def test_easy_http_datetime(
    testing_config: TestingConfigProvider, mock_get_run_details: MagicMock, mock_easy_http_output_requests: MagicMock,
):
    # Given
    testing_config.add("TEST_AUTH_CODE", "a1b2c3d4e5")
    mock_get_run_details.return_value = get_test_data_yaml("job-easy-http-datetime.yml")
    mock_post_response = Mock()
    mock_post_response.status_code = 200
    mock_post_response.content = "This is a test response"
    mock_easy_http_output_requests.post.return_value = mock_post_response

    # When
    run("e1cf1105-defc-4b76-865a-805975dc42e2")

    # Then
    mock_easy_http_output_requests.request.assert_called_once_with(
        "put",
        "https://something.example.com/path/here",
        json={"message": "Date: Tue 29 Dec 2020 19:51:18 UTC", "duration": "30000"},
        headers={"Auth-Token": "a1b2c3d4e5"},
    )


def test_elasticsearch_to_slack(
    testing_config: TestingConfigProvider,
    mock_get_run_details: MagicMock,
    mock_elasticsearch_input_elasticsearch_definition: MagicMock,
    mock_slack_output_requests: MagicMock,
):
    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    mock_get_run_details.return_value = get_test_data_yaml("job-elasticsearch-to-slack.yml")
    mock_elasticsearch_input_elasticsearch_definition.return_value.search.return_value = get_test_data_json(
        "response-elasticsearch.json"
    )
    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    # When
    run("4ce8e56f-90b2-4e43-b2d0-2e4257a6cd34")

    # Then
    mock_slack_output_requests.post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXX",
        json={"text": get_test_data("test_elasticsearch_input---test_elasticsearch_to_slack---expected-details.txt")},
    )


def test_pushover_time(
    testing_config: TestingConfigProvider, mock_get_run_details: MagicMock, mock_pushover_request_post: MagicMock,
):
    # Given
    testing_config.add("PUSHOVER_APP_ID", "azGDORePK8gMaC0QOYAMyEEuzJnyUi")
    testing_config.add("PUSHOVER_GROUP_TEST", "uQiRzpo4DXghDmr9QzzfQu27cmVRsG")
    mock_get_run_details.return_value = get_test_data_yaml("job-pushover-time.yml")
    mock_post_response = Mock()
    mock_post_response.status_code = 200
    mock_post_response.content = "This is a test response"
    mock_pushover_request_post.return_value = mock_post_response

    # When
    run("c313d822-c20f-432e-83f9-4d086d2c329b")

    # Then
    mock_pushover_request_post(
        "https://api.pushover.net/1/messages.json",
        headers={"Content-Type": "application/json"},
        json={
            "token": "azGDORePK8gMaC0QOYAMyEEuzJnyUi",
            "user": "uQiRzpo4DXghDmr9QzzfQu27cmVRsG",
            "message": "Hello World!!! It's currently Thu Dec 31 20:00:00 1998\nHope you are having a good day",
            "device": "droid2",
            "title": "Direct message from @someuser",
            "url": "twitter://direct_message?screen_name=someuser",
            "url_title": "Reply to @someuser",
            "priority": "1",
            "sound": "incoming",
            "timestamp": "1331249662",
        },
    )


def test_advanced_job(
    testing_config: TestingConfigProvider,
    mock_get_run_details: MagicMock,
    mock_open_weather_city_input_requests: MagicMock,
    mock_slack_output_requests: MagicMock,
    mock_stdout_output_write_to_standard_out: MagicMock,
    mock_random_message_input_random_choice: MagicMock,
):
    # Given
    testing_config.add("OPEN_WEATHER_KEY", "a1b2c3")
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    testing_config.add("SLACK_CHANNEL_TEST", "#test")
    mock_get_run_details.return_value = get_test_data_yaml("job-advanced.yml")

    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    mock_open_weather_city_input_requests_get = MagicMock()
    mock_open_weather_city_input_requests_get.status_code = 200
    mock_open_weather_city_input_requests_get.json.return_value = get_test_data_json("response-open-weather-city.json")
    mock_open_weather_city_input_requests.get.return_value = mock_open_weather_city_input_requests_get

    # When
    run("444d3161-2b8f-40a7-aaf1-6d49e8003075")

    # Then
    mock_slack_output_requests.post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXX",
        json={
            "text": "A test at Week 52 (day 364) - Tuesday December 29/12/20\n"
            "The weather is :cloud: on day 364 broken clouds 6.439999999999998c"
            " Weather by Openweathermap (openweathermap.org)",
            "channel": "#test",
            "username": "modular-message-bot",
            "icon_emoji": ":robot_face:",
        },
    )
    mock_stdout_output_write_to_standard_out.assert_has_calls(
        [
            call(
                "A test at Week 52 (day 364) - Tuesday December 29/12/20\n"
                "The weather is broken clouds 6.439999999999998c Weather by Openweathermap"
            ),
            call(
                "Hi! Good Morning! It's going to be broken clouds (Weather by Openweathermap)"
                " I hope you are having a good day :)"
            ),
        ]
    )

    mock_open_weather_city_input_requests.get.assert_has_calls(
        [call("https://api.openweathermap.org/data/2.5/weather", params={"q": "edinburgh,uk", "appid": "a1b2c3"},)]
    )
    mock_random_message_input_random_choice.assert_called_once_with(
        [
            "Good Morning! It's going to be broken clouds (Weather by Openweathermap)",
            "Buongiorno! It's going to be broken clouds (Weather by Openweathermap)",
            "Buenos días! It's going to be broken clouds (Weather by Openweathermap)",
        ]
    )


def test_jobs_simple_run_single(
    testing_config: TestingConfigProvider,
    mock_get_run_details: MagicMock,
    mock_open_weather_city_input_requests: MagicMock,
    mock_slack_output_requests: MagicMock,
    mock_stdout_output_write_to_standard_out: MagicMock,
):
    # Testing if we have a job config with 2 tasks, it will run the first task only

    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXXX")
    testing_config.add("SLACK_CHANNEL", "#weather")
    mock_get_run_details.return_value = get_test_data_yaml("jobs-simple.yml")

    # When
    run("2a424411-7a0a-461f-8d88-313c938c7e24")

    # Then
    mock_slack_output_requests.post.assert_not_called()
    mock_stdout_output_write_to_standard_out.assert_called_once_with("Hi. It's Week 52")

    mock_open_weather_city_input_requests.get.assert_not_called()

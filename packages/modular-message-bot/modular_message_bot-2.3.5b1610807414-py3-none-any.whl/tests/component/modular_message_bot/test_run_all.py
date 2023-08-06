from unittest.mock import MagicMock, Mock, call

from modular_message_bot.run_all import run

from tests.component.conftest import TestingConfigProvider, get_test_data_json, get_test_data_yaml


def test_jobs_simple(
    testing_config: TestingConfigProvider,
    mock_get_run_details: MagicMock,
    mock_open_weather_city_input_requests: MagicMock,
    mock_slack_output_requests: MagicMock,
    mock_stdout_output_write_to_standard_out: MagicMock,
):
    # Given
    testing_config.add("SLACK_URL", "https://hooks.slack.com/services/T00000000/B00000000/XXXXX")
    testing_config.add("SLACK_CHANNEL", "#weather")
    testing_config.add("OPEN_WEATHER_KEY", "a1b2c3")
    mock_get_run_details.return_value = get_test_data_yaml("jobs-simple.yml")

    mock_slack_post_response = Mock()
    mock_slack_post_response.status_code = 200
    mock_slack_output_requests.post.return_value = mock_slack_post_response

    mock_open_weather_city_input_requests_get = MagicMock()
    mock_open_weather_city_input_requests_get.status_code = 200
    mock_open_weather_city_input_requests_get.json.return_value = get_test_data_json("response-open-weather-city.json")
    mock_open_weather_city_input_requests.get.return_value = mock_open_weather_city_input_requests_get

    # When
    run()

    # Then
    mock_slack_output_requests.post.assert_called_once_with(
        "https://hooks.slack.com/services/T00000000/B00000000/XXXXX",
        json={
            "channel": "#weather",
            "username": "WeatherBot",
            "text": "Hello! The weather is broken clouds. Weather by Openweathermap",
            "icon_emoji": ":robot_face:",
        },
    )
    mock_stdout_output_write_to_standard_out.assert_called_once_with("Hi. It's Week 52")

    mock_open_weather_city_input_requests.get.assert_has_calls(
        [call("https://api.openweathermap.org/data/2.5/weather", params={"q": "edinburgh,uk", "appid": "a1b2c3"},)]
    )

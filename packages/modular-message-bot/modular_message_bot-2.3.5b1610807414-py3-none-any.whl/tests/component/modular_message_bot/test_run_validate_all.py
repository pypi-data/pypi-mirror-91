from logging import Logger
from unittest.mock import MagicMock

import pytest
from pytest_mock import MockerFixture

from modular_message_bot.run_validate_all import run

from tests.component.conftest import get_test_data_yaml


@pytest.fixture(autouse=True)
def mock_logger(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.run_validate_all.logger", spec=Logger)


@pytest.fixture(autouse=True)
def mock_exit(mocker: MockerFixture):
    return mocker.patch("modular_message_bot.run_validate_all.exit", spec=exit)


def test_valid_jobs_success(mock_get_run_details: MagicMock, mock_logger: MagicMock, mock_exit: MagicMock):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-advanced.yml")

    # When
    run()

    # Then
    mock_logger.info.assert_called_once_with("Jobs are valid!")
    mock_logger.error.assert_not_called()
    mock_exit.assert_not_called()


def test_valid_jobs_invalid(mock_get_run_details: MagicMock, mock_logger: MagicMock, mock_exit: MagicMock):
    # Given
    mock_get_run_details.return_value = get_test_data_yaml("job-invalid.yml")

    # When
    run()

    # Then
    mock_exit.assert_called_once_with("Jobs are invalid")
    mock_logger.error.assert_called_once_with(
        "'search' is required for 'elasticsearch' input."
        " See https://elasticsearch-py.readthedocs.io"
        "/en/7.10.0/api.html?highlight=search#elasticsearch.Elasticsearch.search"
    )
    mock_logger.info.assert_not_called()

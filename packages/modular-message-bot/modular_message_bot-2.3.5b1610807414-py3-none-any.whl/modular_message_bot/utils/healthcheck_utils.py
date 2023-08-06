from pathlib import Path

from modular_message_bot.config.config_collection import ConfigCollection


def healthcheck_liveness_file(config: ConfigCollection):
    file = config.get("HEALTHCHECK_LIVENESS_FILE", "")
    if file != "":
        Path(file).touch()


def healthcheck_readiness_file(config: ConfigCollection):
    file = config.get("HEALTHCHECK_READINESS_FILE", "")
    if file != "":
        Path(file).touch()

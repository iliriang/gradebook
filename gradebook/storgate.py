"""JSON persistence helpers for gradebook data."""

import json
from json import JSONDecodeError
from pathlib import Path

from .logging_config import get_logger

DEFAULT_DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "gradebook.json"
LOGGER = get_logger(__name__)


def _empty_data() -> dict:
    return {
        "students": [],
        "courses": [],
        "enrollments": [],
        "next_student_id": 1,
    }


def load_data(path: Path | str = DEFAULT_DATA_PATH) -> dict:
    """Load gradebook data from JSON, returning an empty structure if missing."""
    data_path = Path(path)
    try:
        with data_path.open("r", encoding="utf-8") as file:
            data = json.load(file)
        LOGGER.info("Loaded data from %s", data_path)
        return data
    except FileNotFoundError:
        LOGGER.info("Data file not found at %s. Starting with empty dataset.", data_path)
        return _empty_data()
    except JSONDecodeError as exc:
        message = (
            f"Data file '{data_path}' is invalid JSON. "
            "Please fix or delete the file and try again."
        )
        LOGGER.error("%s Error: %s", message, exc)
        print(message)
        return _empty_data()
    except OSError as exc:
        LOGGER.error("Failed to read data file %s: %s", data_path, exc)
        raise RuntimeError(f"Failed to read data file: {exc}") from exc


def save_data(data: dict, path: Path | str = DEFAULT_DATA_PATH) -> None:
    """Save gradebook data to JSON with safe directory creation."""
    data_path = Path(path)
    data_path.parent.mkdir(parents=True, exist_ok=True)

    try:
        with data_path.open("w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
        LOGGER.info("Saved data to %s", data_path)
    except OSError as exc:
        LOGGER.error("Failed to save data to %s: %s", data_path, exc)
        raise RuntimeError(f"Failed to save data file: {exc}") from exc

from __future__ import annotations

from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Optional

from deepdiff import DeepDiff

from .config import SessionConfiguration, _parse_yaml_file_to_config


def diff_yaml_config_with_python_config(
    yaml_config: str, python_config: SessionConfiguration
) -> Optional[DeepDiff]:
    with NamedTemporaryFile(delete=False, mode="w", prefix="atoti-") as file:
        try:
            file.write(yaml_config)
            file.close()
            parsed_yaml_config = _parse_yaml_file_to_config(Path(file.name))
        finally:
            Path(file.name).unlink()

    # Return None when the diff is empty so that interactive examples can have omit the output line when the configs are equal.
    return DeepDiff(parsed_yaml_config, python_config) or None

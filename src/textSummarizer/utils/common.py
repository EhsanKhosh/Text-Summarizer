import os
from box.exceptions import BoxValueError
import yaml
from textSummarizer.logging import logger
from ensure import ensure_annotations
from pathlib import Path
from box import ConfigBox
from typing import Any



def read_yaml(filename: Path) -> Any:
    try:
        with open(filename, 'r') as stream:
            content = yaml.safe_load(stream)
            logger.info(f"Loaded {filename}")
            return ConfigBox(content)
    except BoxValueError:
        raise ValueError(f"yaml file is empty: {filename}")
    except Exception as e:
        raise e


def create_dirs(paths: list, verbose: bool = True) -> None:
    for path in paths:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"create directory at {path}")


@ensure_annotations
def get_size(path_to_file: str) -> int:
    return f'{os.path.getsize(path_to_file)}'

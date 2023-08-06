import logging
import math
from pathlib import Path
from sys import exit
from typing import List

from more_itertools import chunked

from .program_config import ProgramConfig

logger = logging.getLogger(__name__)


def main(program_config: ProgramConfig):
    ensure_destination_directory(program_config)
    maybe_sort_files(program_config)

    for chunk_number, chunk in enumerate(
        chunked(program_config.files, program_config.number_per_folder), start=1
    ):
        logger.debug(f"chunk {chunk_number}, containing {len(chunk)} items")

        sub_folder_postfix = pad_sub_folder_number(chunk_number, program_config)

        sub_folder = program_config.destination_directory.joinpath(
            f"{program_config.sub_folder_prefix}{sub_folder_postfix}"
        )

        ensure_sub_folder(sub_folder)

        for file in chunk:
            if not file.is_file():
                logger.info(
                    f"A supplied path, {file.absolute()}, does not exist or is not a file. Skipping."
                )
                continue
            file.rename(sub_folder.joinpath(file.name))


def ensure_destination_directory(program_config: ProgramConfig):
    if (
        program_config.destination_directory.exists()
        and not program_config.destination_directory.is_dir()
    ):
        logger.error(
            f"The supplied destination {program_config.destination_directory.absolute()} exists but isn't a directory. Aborting."
        )
        exit(1)

    program_config.destination_directory.mkdir(exist_ok=True)


def ensure_sub_folder(sub_folder: Path):
    if sub_folder.is_dir():
        logger.info(
            f"A sub-folder, {sub_folder.absolute()}, already exists. Continuing."
        )
    elif sub_folder.exists():
        logger.error(
            f"A required sub-folder {sub_folder.absolute()} already exists but isn't a directory. Aborting."
        )
        exit(1)
    else:
        sub_folder.mkdir()


def maybe_sort_files(program_config: ProgramConfig):
    if program_config.sort:
        program_config.files = sort_list_of_paths(program_config.files)
        logging.debug(program_config.files[:10])


def pad_sub_folder_number(number: int, program_config: ProgramConfig) -> str:
    max_number = len(program_config.files) + 1
    max_width = math.floor(math.log10(max_number)) + 1
    return str(number).rjust(max_width, "0")


def sort_list_of_paths(list_of_paths: List[Path]):
    from natsort import natsorted

    list_of_strings = list(str(path.absolute()) for path in list_of_paths)
    sorted_list_of_strings = natsorted(list_of_strings)
    return list(Path(string) for string in sorted_list_of_strings)
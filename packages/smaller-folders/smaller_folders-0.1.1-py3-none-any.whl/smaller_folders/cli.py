import argparse
import logging
from pathlib import Path

from .program_config import ProgramConfig
from . import core

logger = logging.getLogger(__name__)


def main():
    logger.debug("Invoked at cli.py:main")

    config = ArgumentParser().parse_args_to_config()
    configure_root_logger(config)
    logger.debug(config)

    core.main(config)


class ArgumentParser(argparse.ArgumentParser):
    def __init__(self, *args, **kwargs):
        super().__init__(
            *args,
            **kwargs,
            # NOTE this must be kept in sync with pyproject.toml
            description="Split an arbitrary number of files into sub-folders containing a specified number of files each.",
        )
        self.add_argument(
            "-l",
            "--log-level",
            choices=[
                "debug",
                "info",
                "error",
            ],
            default="info",
            help="set logging level for this tool",
            type=str,
        )
        self.add_argument(
            "-d",
            "--destination-directory",
            help="the directory in which to create sub-folders (which will, in turn, contain the moved files)",
            required=True,
            type=Path,
        )
        self.add_argument(
            "-f",
            "--files",
            help="the names of the files to be moved to the sub-folders",
            metavar="FILE",
            nargs="+",
            required=True,
            type=Path,
        )
        self.add_argument(
            "-n",
            "--number-per-folder",
            help="the maximum number of files each sub-folder should contain",
            required=True,
            type=int,
        )
        self.add_argument(
            "-p",
            "--sub-folder-prefix",
            help="the subfolders will be named SUB_FOLDER_PREFIX001 and so on. Default is 'smaller_folder'",
            default="smaller_folder",
            type=str,
        )
        self.add_argument(
            "-s",
            "--sort",
            action="store_true",
            default=False,
            help="naturally (not lexicographically) sort the supplied files",
        )

    def parse_args_to_config(self, *args, **kwargs) -> ProgramConfig:
        args = self.parse_args(*args, **kwargs)
        return ProgramConfig(
            log_level=args.log_level,
            destination_directory=args.destination_directory,
            files=args.files,
            number_per_folder=args.number_per_folder,
            sub_folder_prefix=args.sub_folder_prefix,
            sort=args.sort,
        )


def configure_root_logger(program_config: ProgramConfig):
    root_logger = logging.getLogger()
    root_logger.setLevel(
        level=getattr(
            logging,
            program_config.log_level.upper(),
        )
    )
    handler = logging.StreamHandler()
    formatter = logging.Formatter("%(name)-20s: %(levelname)5s: %(message)s")
    handler.setFormatter(formatter)
    root_logger.addHandler(handler)
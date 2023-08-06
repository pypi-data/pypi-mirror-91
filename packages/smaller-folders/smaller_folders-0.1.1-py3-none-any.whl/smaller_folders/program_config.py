import dataclasses
from pathlib import Path
from typing import List


@dataclasses.dataclass
class ProgramConfig:
    log_level: str
    destination_directory: Path
    files: List[Path]
    number_per_folder: int
    sub_folder_prefix: str
    sort: bool

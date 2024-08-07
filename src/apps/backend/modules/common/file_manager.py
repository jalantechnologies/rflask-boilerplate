from typing import IO, Any


class FileManager:
    def __init__(self, filename: str, mode: str) -> None:
        self.file: IO
        self.filename = filename
        self.mode = mode

    def __enter__(self) -> IO[Any]:
        self.file = open(self.filename, self.mode)
        return self.file

    def __exit__(self, exc_type: str, exc_value: str, exc_traceback: str) -> None:  # noqa
        self.file.close()

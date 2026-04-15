"""Custom exceptions for MiniOS filesystem operations."""


class FileSystemError(Exception):
    """Base exception for all MiniOS filesystem errors."""

    default_message = "filesystem error"

    def __init__(self, message: str | None = None) -> None:
        super().__init__(message or self.default_message)


class PathNotFoundError(FileSystemError):
    """Raised when a path cannot be resolved."""

    default_message = "path not found"


class AlreadyExistsError(FileSystemError):
    """Raised when creating an entry that already exists."""

    default_message = "entry already exists"


class InvalidOperationError(FileSystemError):
    """Raised when an operation is not valid for a target."""

    default_message = "invalid operation"


class NotAFileError(FileSystemError):
    """Raised when a file was expected but found otherwise."""

    default_message = "not a file"


class NotADirectoryError(FileSystemError):
    """Raised when a directory was expected but found otherwise."""

    default_message = "not a directory"

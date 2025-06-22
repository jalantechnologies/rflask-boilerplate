class TodoError(Exception):
    """Base class for all TODO-related errors."""

    def __init__(self, message: str, code: str):
        super().__init__(message)
        self.code = code


class TodoNotFoundError(TodoError):
    def __init__(self, todo_id: str):
        super().__init__(f"Todo with ID '{todo_id}' not found.", code="TODO_NOT_FOUND")


class InvalidDueDateFormatError(TodoError):
    def __init__(self, date_str: str):
        super().__init__(f"Due date '{date_str}' is not in a valid ISO format.", code="INVALID_DUE_DATE_FORMAT")

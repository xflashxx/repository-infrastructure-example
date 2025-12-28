from fastapi import status


class HTTPError(Exception):
    """
    Base HTTP exception class to represent HTTP errors.
    """

    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    detail = "Internal Server Error"

    def __init__(self, *, status_code: int, detail: str) -> None:
        self.status_code = status_code
        self.detail = detail
        super().__init__(self.detail)

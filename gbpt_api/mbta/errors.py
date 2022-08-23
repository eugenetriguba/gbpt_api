import fastapi
import requests


class MBTAError(Exception):
    def __init__(
        self, response: requests.Response, message: str | None = None
    ) -> None:
        if message is None:
            message = f"{response.status_code} - {response.reason}"

        super().__init__(message)
        self.status_code = response.status_code
        self.reason = response.reason


class APIError(MBTAError):
    """Used to denote a generic >= 4xx error code from the MBTA API."""

    def __init__(self, response: requests.Response) -> None:
        super().__init__(response)


class RateLimitExceededError(MBTAError):
    """MBTA API rate limit has exceeded."""

    def __init__(self, response: requests.Response):
        self.rate_limit_reset = response.headers.get("x-ratelimit-reset")
        super().__init__(
            response,
            f"MBTA rate limit exceeded. Resets at: {self.rate_limit_reset}.",
        )


def get_api_error(response: requests.Response) -> MBTAError:
    """Retrieve errors based on the request response."""
    if response.status_code == fastapi.status.HTTP_429_TOO_MANY_REQUESTS:
        return RateLimitExceededError(response)
    else:
        return APIError(response)

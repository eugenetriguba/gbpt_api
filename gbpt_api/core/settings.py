from decouple import config  # type: ignore

MBTA_API_KEY: str = config("MBTA_API_KEY", default="")

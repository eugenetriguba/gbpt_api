from .routes import router as stops_router


def get_routers():
    """Hook used by the app to find the routers."""
    return [stops_router]

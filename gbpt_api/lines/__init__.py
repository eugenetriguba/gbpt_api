from .routes import router as lines_router


def get_routers():
    """Hook used by the app to find the routers."""
    return [lines_router]

from pathlib import Path
from typing import Union

from fastapi import FastAPI

from gbpt_api.core.logger import configure_logger, get_logger
from gbpt_api.core.utils import combine_module_attrs, module_path

logger = get_logger(__name__)


def run_api() -> FastAPI:
    """Starts up the backend API.

    Returns:
        A FastAPI instance with all the API routers
        from the modules included.
    """
    configure_logger()

    app = FastAPI(title="Greater Boston Public Transit API")
    app = _attach_api_routers(app, module_path())

    return app


def _attach_api_routers(app: FastAPI, path: Union[str, Path]) -> FastAPI:
    """Attaches the API routers from the modules onto the fastAPI app.

    Args:
        app: The FastAPI app to attach routers to.
        path: The path to retrieve routers from.

    Returns:
        A FastAPI app with the routers included.
    """
    routers = combine_module_attrs("get_routers", path)

    for router in routers:
        app.include_router(router, prefix="/v1")

    return app

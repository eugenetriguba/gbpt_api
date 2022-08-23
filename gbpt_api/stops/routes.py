import fastapi

from gbpt_api import mbta
from gbpt_api.core.logger import get_logger

logger = get_logger(__name__)
router = fastapi.APIRouter()


@router.get("/stops")
async def get_stops(line: str | None = None):
    stops = mbta.Client().list_stops(route_ids=line)

    response = []
    for stop in stops:
        response.append({"id": stop["id"]})

    return response

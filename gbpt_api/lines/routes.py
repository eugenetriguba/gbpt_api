import enum

import fastapi

from gbpt_api import mbta
from gbpt_api.core.logger import get_logger

logger = get_logger(__name__)
router = fastapi.APIRouter()


class LineType(enum.Enum):
    HEAVY_RAIL = mbta.RouteType.HEAVY_RAIL.name.lower()

    def to_route_type(self) -> mbta.RouteType:
        return mbta.RouteType[self.name]


@router.get("/lines")
async def get_lines(type: LineType | None = None):
    if type is not None:
        route_type = type.to_route_type()
    else:
        route_type = None

    routes = mbta.Client().list_routes(type=route_type)

    response = []
    for route in routes:
        response.append(
            {
                "id": route["id"],
                "name": route["attributes"]["long_name"],
            }
        )

    return response

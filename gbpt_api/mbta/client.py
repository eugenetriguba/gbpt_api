import enum
import urllib.parse

import requests

from gbpt_api.core import settings
from gbpt_api.core.logger import get_logger
from gbpt_api.mbta import errors

logger = get_logger(__name__)


class RouteType(enum.Enum):
    """Accepted route types.

    Reference:
        - https://github.com/google/transit/blob/master/gtfs/spec/en/reference.md#routestxt  # noqa: E501
        - https://api-v3.mbta.com/docs/swagger/index.html#/Route/ApiWeb_RouteController_index  # noqa: E501
    """

    # Subway, Metro. Any underground rail system within a metropolitan area.
    HEAVY_RAIL = 1


class Client:
    API_URI = "https://api-v3.mbta.com"
    API_KEY = settings.MBTA_API_KEY

    def list_routes(
        self, type: RouteType | list[RouteType] | None = None
    ) -> list[dict]:
        """Make a GET /routes call to the MBTA API.

        Args:
            type: The type of route to filter by.

        Returns:
            A list of routes.

            Sample schema of a route:
                {
                    "attributes": {
                        "color": "ED8B00",
                        "description": "Rapid Transit",
                        "direction_destinations": [
                        "Forest Hills",
                        "Oak Grove"
                        ],
                        "direction_names": [
                        "South",
                        "North"
                        ],
                        "fare_class": "Rapid Transit",
                        "long_name": "Orange Line",
                        "short_name": "",
                        "sort_order": 10020,
                        "text_color": "FFFFFF",
                        "type": 1
                    },
                    "id": "Orange",
                    "links": {
                        "self": "/routes/Orange"
                    },
                    "relationships": {
                        "line": {
                            "data": {
                                "id": "line-Orange",
                                "type": "line"
                            }
                        }
                    },
                    "type": "route"
                }
        """
        query_parameters = {"type": self._join(type, ",")}

        response = self._make_request(
            "GET",
            "routes",
            query_parameters=query_parameters,
        )

        return response["data"]

    def list_stops(
        self, route_ids: str | list[str] | None = None
    ) -> list[dict]:
        """Make a GET /stops call to the MBTA  API.

        Args:
            route_ids: The route IDs to use to filter this response by.

        Returns:
            A list of stops.

            Sample schema of a stop:
                {
                    "attributes": {
                        "address": "Alewife Brook Pkwy and Cambridge Park Dr, Cambridge, MA 02140",  # noqa: E501
                        "at_street": null,
                        "description": null,
                        "latitude": 42.395428,
                        "location_type": 1,
                        "longitude": -71.142483,
                        "municipality": "Cambridge",
                        "name": "Alewife",
                        "on_street": null,
                        "platform_code": null,
                        "platform_name": null,
                        "vehicle_type": null,
                        "wheelchair_boarding": 1
                    },
                    "id": "place-alfcl",
                    "links": {
                        "self": "/stops/place-alfcl"
                    },
                    "relationships": {
                        "facilities": {
                            "links": {
                                "related": "/facilities/?filter[stop]=place-alfcl"  # noqa: E501
                            }
                        },
                        "parent_station": {
                            "data": null
                        },
                        "zone": {
                            "data": null
                        }
                    },
                    "type": "stop"
                }
        """
        query_parameters = {"route": self._join(route_ids, ",")}

        response = self._make_request(
            "GET",
            "stops",
            query_parameters=query_parameters,
        )

        return response["data"]

    def _join(
        self, items: enum.Enum | str | list | None, delim: str
    ) -> str | None:
        """Join a list of enums or strings by delim.

        Args:
            items: The items to join together.
            delim: The delimiter to join `items` by.

        Returns:
            A string of items separated by `delim` or None if
            `items` is "falsey".
        """
        if not items:
            return None

        if not isinstance(items, list):
            items = [items]

        join_elements = []
        for item in items:
            if isinstance(item, enum.Enum):
                join_elements.append(str(item.value))
            else:
                join_elements.append(str(item))

        return delim.join(join_elements)

    def _make_request(
        self,
        method: str,
        resource: str,
        query_parameters: dict | None = None,
    ) -> dict:
        """Make a request to the MBTA API.

        Args:
            method: The HTTP method to use.
            resource: The resource to make a request to.
            query_parameters: An optional set of query parameters to
                filter the response by.

        Raises:
            An MBTAError if the response is a >= 4xx status code.

        Returns:
            The data portion of the JSON response.
        """
        uri = self._create_uri(resource, query_parameters=query_parameters)
        logger.debug(f"Calling {method} {uri}")

        requests_method = getattr(requests, method.lower())
        response = requests_method(
            uri,
            headers={
                "Accept-Encoding": "gzip",
                "Content-Type": "application/vnd.api+json",
            },
        )
        if not response.ok:
            raise errors.get_api_error(response)

        data = response.json()
        logger.debug(
            {
                "message": "MBTA response",
                "data": data,
                "headers": response.headers,
            }
        )
        return data

    def _create_uri(
        self, resource: str, query_parameters: dict | None = None
    ) -> str:
        """Create a full uri for resource.

        Args:
            resource: The resource we want to join. i.e. /routes
            query_parameters: An optional set of query parameters to
                attach onto the uri. If any values are set to None,
                they will be skipped over.

        Returns:
            A joined and encoded uri.
        """
        uri = urllib.parse.urljoin(self.API_URI, resource)

        if query_parameters:
            if self.API_KEY:
                query_parameters["api_key"] = self.API_KEY

            params_with_values = {
                key: value
                for key, value in query_parameters.items()
                if value is not None
            }
            uri += f"?{urllib.parse.urlencode(params_with_values)}"

        return uri

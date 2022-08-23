import pytest
import requests_mock
from schema import And, Or, Schema  # type: ignore

from gbpt_api import mbta

route_schema = Schema(
    {
        "id": And(str, lambda id: len(id) > 0),
        "attributes": {
            "color": str,
            "description": str,
            "direction_destinations": list,
            "direction_names": list,
            "fare_class": str,
            "long_name": str,
            "short_name": str,
            "sort_order": int,
            "text_color": And(str, lambda hex: len(hex) == 6),
            "type": int,
        },
        "links": dict,
        "relationships": dict,
        "type": "route",
    }
)

stop_schema = Schema(
    {
        "id": And(str, lambda id: len(id) > 0),
        "attributes": {
            "address": Or(None, str),
            "at_street": Or(None, str),
            "description": Or(None, str),
            "latitude": Or(None, float),
            "location_type": int,
            "longitude": Or(None, float),
            "municipality": str,
            "name": str,
            "on_street": Or(None, str),
            "platform_code": Or(None, str),
            "platform_name": Or(None, str),
            "vehicle_type": Or(None, int),
            "wheelchair_boarding": int,
        },
        "links": dict,
        "relationships": dict,
        "type": "stop",
    }
)


@pytest.mark.vcr
def test_list_routes_schema():
    """
    Ensure that a MBTA GET /routes response has the expected
    schema.
    """
    client = mbta.Client()

    response = client.list_routes()

    for route in response:
        assert route_schema.validate(route)


@pytest.mark.vcr
def test_list_routes_with_type_query_param():
    """
    Ensure that a MBTA GET /routes?type=<type> response has a
    filtered response.
    """
    client = mbta.Client()

    response = client.list_routes(type=mbta.RouteType.HEAVY_RAIL)

    for route in response:
        assert route_schema.validate(route)
        assert route["attributes"]["type"] == mbta.RouteType.HEAVY_RAIL.value


@pytest.mark.vcr
def test_list_stops_schema():
    """
    Ensure that a MBTA GET /stops response has the expected
    schema.
    """
    client = mbta.Client()

    response = client.list_stops()

    assert isinstance(response, list)
    assert stop_schema.validate(response[0])


@pytest.mark.vcr
def test_list_stop_with_route_query_param():
    """
    Ensure that a MBTA GET /stops?route=<route> response has a
    filtered response.
    """
    client = mbta.Client()

    response = client.list_stops(route_ids="Red")

    for stop in response:
        assert stop_schema.validate(stop)


@pytest.mark.parametrize(
    "status_code,error",
    [(400, mbta.APIError), (429, mbta.RateLimitExceededError)],
)
def test_4xx_code_on_response(status_code, error):
    client = mbta.Client()

    with pytest.raises(error):
        with requests_mock.Mocker() as mock:
            mock.get(f"{client.API_URI}/routes", status_code=status_code)
            client.list_routes()

import json

import fastapi
import requests_mock
import pytest
from fastapi.testclient import TestClient

from gbpt_api import mbta
from gbpt_api.core.app import run_api

test_client = TestClient(run_api())

LIGHT_RAIL_ENTRY = {
    "attributes": {
        "color": "DA291C",
        "description": "Rapid Transit",
        "direction_destinations": ["Mattapan", "Ashmont"],
        "direction_names": ["Outbound", "Inbound"],
        "fare_class": "Rapid Transit",
        "long_name": "Mattapan Trolley",
        "short_name": "",
        "sort_order": 10011,
        "text_color": "FFFFFF",
        "type": 0,
    },
    "id": "Mattapan",
    "links": {"self": "/routes/Mattapan"},
    "relationships": {
        "line": {"data": {"id": "line-Mattapan", "type": "line"}}
    },
    "type": "route",
}
HEAVY_RAIL_ENTRY = {
    "attributes": {
        "color": "DA291C",
        "description": "Rapid Transit",
        "direction_destinations": ["Ashmont/Braintree", "Alewife"],
        "direction_names": ["South", "North"],
        "fare_class": "Rapid Transit",
        "long_name": "Red Line",
        "short_name": "",
        "sort_order": 10010,
        "text_color": "FFFFFF",
        "type": 1,
    },
    "id": "Red",
    "links": {"self": "/routes/Red"},
    "relationships": {"line": {"data": {"id": "line-Red", "type": "line"}}},
    "type": "route",
}


def test_get_routes(create_api_path):
    endpoint = create_api_path("/lines")
    mock_response = {
        "data": [LIGHT_RAIL_ENTRY, HEAVY_RAIL_ENTRY],
        "jsonapi": {"version": "1.0"},
    }

    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(
            mbta.Client.API_URI + "/routes", text=json.dumps(mock_response)
        )
        response = test_client.get(endpoint)

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == [
        {
            "id": LIGHT_RAIL_ENTRY["id"],
            "name": LIGHT_RAIL_ENTRY["attributes"]["long_name"],
        },
        {
            "id": HEAVY_RAIL_ENTRY["id"],
            "name": HEAVY_RAIL_ENTRY["attributes"]["long_name"],
        },
    ]


@pytest.mark.vcr
def test_get_routes_filter(create_api_path):
    endpoint = create_api_path("/lines?type=heavy_rail")

    response = test_client.get(endpoint)

    assert response.status_code == fastapi.status.HTTP_200_OK


def test_get_routes_invalid_filter(create_api_path):
    endpoint = create_api_path("/lines?type=invalid_type")

    response = test_client.get(endpoint)

    assert response.status_code == fastapi.status.HTTP_422_UNPROCESSABLE_ENTITY

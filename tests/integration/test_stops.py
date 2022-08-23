import json

import fastapi
import requests_mock
import pytest
from fastapi.testclient import TestClient

from gbpt_api import mbta
from gbpt_api.core.app import run_api

test_client = TestClient(run_api())

SAMPLE_STOP = {
    "attributes": {
        "address": None,
        "at_street": None,
        "description": "Chinatown - Bottom of stairs between landing and lobby",
        "latitude": None,
        "location_type": 3,
        "longitude": None,
        "municipality": "Boston",
        "name": "Chinatown",
        "on_street": None,
        "platform_code": None,
        "platform_name": None,
        "vehicle_type": None,
        "wheelchair_boarding": 1,
    },
    "id": "node-chncl-fhlower-lobby",
    "links": {"self": "/stops/node-chncl-fhlower-lobby"},
    "relationships": {
        "facilities": {
            "links": {
                "related": "/facilities/?filter[stop]=node-chncl-fhlower-lobby"
            }
        },
        "parent_station": {"data": {"id": "place-chncl", "type": "stop"}},
        "zone": {"data": None},
    },
    "type": "stop",
}


def test_get_stops(create_api_path):
    endpoint = create_api_path("/stops")
    mock_response = {"data": [SAMPLE_STOP], "jsonapi": {"version": "1.0"}}

    with requests_mock.Mocker(real_http=True) as mock:
        mock.get(mbta.Client.API_URI + "/stops", text=json.dumps(mock_response))
        response = test_client.get(endpoint)

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == [{"id":SAMPLE_STOP["id"]}]


@pytest.mark.vcr
def test_get_stops_filter(create_api_path):
    endpoint = create_api_path("/stops?line=Red")

    response = test_client.get(endpoint)

    assert response.status_code == fastapi.status.HTTP_200_OK


@pytest.mark.vcr
def test_get_routes_filter_with_no_responses(create_api_path):
    endpoint = create_api_path("/stops?line=abc132509invalid")

    response = test_client.get(endpoint)

    assert response.status_code == fastapi.status.HTTP_200_OK
    assert response.json() == []

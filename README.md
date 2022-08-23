# Greater Boston Public Transit API

This small application integrates with the [Massachusetts Bay Transportation Authority](https://api-v3.mbta.com/) (MBTA) API to show subway lines and stops in the Greater Boston area.

## How to start up the API

The project uses Docker containers with Docker Compose to run the API. In order to run the project, you'll want to have `docker` and `docker-compose` installed.

After that, we'll want to copy in the `.env` file. If you have a MBTA API key to use, this would be where you would want to paste that in. However, you do not need one. You'll just have a lower limit of requests per minute if you choose not to use one.

```
$ cp .env.template .env
```

Then, we can bring up the container.

```
$ docker-compose up -d
```

Lastly, you can navigate to `http://localhost:8000/docs#/` to see the exposed routes.

## Using the API

The API is designed as a REST API. It exposes two resources: `lines` and `stops`. `lines` allows you to filter for only subway lines. Furthermore, `stops` allows you to filter for only stops on particular lines. There is no authentication required to use any route.

So, let's play around and get a feel for this API.

When we call `/v1/lines`, we get a response of IDs and names of the lines.

```bash
$ curl "http://localhost:8000/v1/lines"
[{"id":"Red","name":"Red Line"},{"id":"Mattapan","name":"Mattapan Trolley"},...]
```

Then we can also filter those lines to only "heavy_rail" (subway or metro) lines.

```bash
$ curl "http://localhost:8000/v1/lines?type=heavy_rail"
[{"id":"Red","name":"Red Line"},{"id":"Orange","name":"Orange Line"},{"id":"Blue","name":"Blue Line"}]
```

- Try passing a value for `type` that isn't allowed, such as "heavy", what happens?

Now let's say we're curious about the stops. By calling `/v1/stops`, we can get a list of IDs for all the stops.

```bash
$ curl "http://localhost:8000/v1/stops"
[...,{"id":"place-ER-0128"},{"id":"4673"},{"id":"23841"},{"id":"8852"},{"id":"3945"},{"id":"6201"},{"id":"8823"},{"id":"46734"},{"id":"door-unsqu-ramp"},...]
```

Furthermore, we can limit that list to just the particular stops for a line.

```bash
$ curl "http://localhost:8000/v1/stops?line=Red"
[{"id":"place-alfcl"},{"id":"place-davis"},{"id":"place-portr"},{"id":"place-harsq"},{"id":"place-cntsq"},{"id":"place-knncl"},{"id":"place-chmnl"},{"id":"place-pktrm"},{"id":"place-dwnxg"},{"id":"place-sstat"},{"id":"place-brdwy"},{"id":"place-andrw"},{"id":"place-jfk"},{"id":"place-shmnl"},{"id":"place-fldcr"},{"id":"place-smmnl"},{"id":"place-asmnl"},{"id":"place-nqncy"},{"id":"place-wlsta"},{"id":"place-qnctr"},{"id":"place-qamnl"},{"id":"place-brntn"}]
```

## API Reference

The API specification is automatically generated according to the OpenAPI specification (`http://localhost:8000/openapi.json`). Once you've started up the application, `http://localhost:8000/docs#/` provides an interactive API reference that you may consult.

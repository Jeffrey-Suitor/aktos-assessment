# Aktos Backend Engineering Take Home

Write an API endpoint that uses request params to filter the set of consumers from the data provided by the [CSV](https://drive.google.com/file/d/1gzh1GczznM8p-qW0UNm4H9HLnydXnf6Q/view?usp=sharing). Please submit solutions in the form of a readme + working code.

Sample API requests:
1. `GET /consumers?min_previous_jobs_count=2&max_previous_jobs_count=3&status=active`
2. `GET /consumers?previous_jobs_count=3&status=collected`

Allowed parameters to the endpoint:

1. **min_previous_jobs_count**: The min number of previous jobs held.
2. **max_previous_jobs_count**: The max number of previous jobs held.
3. **previous_jobs_count**: The exact number of previous jobs held.
4. **status**: The status of the debt collected.

The expected response is a GeoJSON FeatureCollection of consumers:
```
{
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {"type": "Point", "coordinates": [-111.92,33.45]},
      "properties": {
        "id": "4", # CSV id
        "amount_due": 1001,
        "previous_jobs_count": 1,
        "status": "in_progress",
        "street": "346 Euclid Wl"
      }
    },
    ...
  ]
}
```


All query parameters are optional, and the minimum and maximum fields should be inclusive (e.g. min_previous_jobs_count=2&max_previous_jobs_count=3 should return consumers that have held 2-3 previous jobs).

## Minimum Requirements
- Your API endpoint URL is /consumers
- Your API responds with valid GeoJSON (you can check the output using http://geojson.io)
- Your API should correctly filter any combination of API parameters
- Use a datastore

## Bonus Points
- Pagination via web linking (http://tools.ietf.org/html/rfc5988)
- Tests for the endpoint
- Adding some level of rate-limiting

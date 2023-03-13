# Aktos Assessment - Jeff Suitor

## Overview

This is Jeff Suitor's Aktos assessment. This project consists of a django project deployed on railway along with a remote postgres database. This project includes the required base functionality for the task as well as all optional functionality.

## Setup and Usage
```bash
pip install -r requirements.txt
```
To run a local instance you can uncomment the sqlite and comment the postgres dbs in settings.py If you do run the following command
```bash
python3 manage.py migrate
```
Finally run the server locally
```bash
python3 manage.py runserver
```
For testing run 
```bash
python3 manage.py test
```

## Requirements
### Minimum
- *Your API endpoint URL is /consumers* --> Deployed at https://aktos-assessment.up.railway.app/consumers
- *Your API responds with valid GeoJSON (you can check the output using http://geojson.io)* --> Done + testing
- *Your API should correctly filter any combination of API parameters* --> Done + testing
- *Use a datastore* --> Deployed at https://railway.app/project/c7797985-ee3b-4913-8ea4-b7ddbe730e7d, see api_consumer table

### Optional

- *Pagination via web linking (http://tools.ietf.org/html/rfc5988)* Done, see the paginators.py file for implementation
- *Tests for the endpoint* --> See the tests folder inside api for endpoint as well as other testing
- *Adding some level of rate-limiting* --> Configured globally but only for ip but it's a start. Rate limiting is 30 requests per minute for burst traffic and 500 requests per day for continous traffic. See the REST_FRAMEWORK dictionary in settings.py. There is also a demo test for this
## Note

- It should be noted that I did chose to use the Django Rest Framework. In hindsight it wasn't really necessary but it did make the experience a bit nicer to work with. It made the throttling section much easier and I had also been hoping to use their pagination tooling but I couldn't find a solution I loved so I just implemented it myself. If I were to do it again given more time I probably would have just used plain django.

- The API is set to throttle at 30 request per minute and 500 requests per day. 

- Page size is initially set to 10 but can be controlled via the page_size query param and the page query_param can be used to select a page.

- I've squashed all my commits down before submitting since that would be my normal workflow and also quite a bit of my commits were related to getting the deployment set up.
## Next Steps

- I built this using minimal type annotations so given more that I would likely add those. Maybe look into a validation library or something to make sure that I am not missing any edge cases for the api and to make the validation process a bit nicer.

- Add user identification and authentication if the next endpoints called for it

- I could have added more tests and properly set up a coverage report. Also, my testing configuration was not ideal as it uses a remote postgres database, which while usable was slow. If I had more time I would have likely setup a local instance of postgres and used that for testing but due to the time constraints it wasn't a high priority.

- If given more time and there is a need I could look to setup caching

- I could setup up redirection or errors if page is below 1 or above the max count. For simplicity I just set the minimum to 1 or the max page count but it would have been nice to be able to properly handle that. It also means that while my link urls will still function correctly, they will themselves contain the incorrect query params due to the way I decided to handle their creation.

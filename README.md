# Delivery API
This is an API for a Delivery Service

### About
In this project, I'm using Python 3.6, Django 3 and PostgreSQL with PostGis. I also use the Django Rest Framework (DRF), a powerful library for building APIs that allows high productivity. To focus on the functionalities first, I left the Docker Compose implementation for last. During the development, I used the branch dev in GitHub, making a pull to the master at the end. To validate the project, I recommend using the browser. I hope you like the result presented. I am available for any questions.

In this document, we will talk about:

 - API Routes
 - Installation
 - Test

## API Routes
#### Create a Partner (only for superuser)
Assuming only admins can register, to perform this action, the user needs to be logged as superuser.

| Field | Description  |
|--|--|
| URL | [/api/v1/partners/](http://localhost:8000/api/v1/partners/) |
| Method | `POST` |
| URL Params | **Required** <br> None <br><br> **Optional** <br> None |
| Data Params | `{owner_name: [string], trading_name: [string], document: [string], address: [Point coordinate], coverage_area: [MultiPolygon coordinate]}` <br><br> **Example** <br> `{"trading_name": "Adega da Cerveja - Pinheiros", "owner_name": "Zé da Silva", "document": "11.666.231/0001-01", "coverage_area": {  "type": "MultiPolygon",  "coordinates": [ [[[30, 20], [45, 40], [10, 40], [30, 20]]],  [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]] ] }, "address": {  "type": "Point", "coordinates": [-46.57421, -21.785741]}}` |
| Samples Call | `curl -d '{"trading_name": "Adega da Cerveja - Pinheiros", "owner_name": "Zé da Silva", "document": "11.666.231/0001-01", "coverage_area": {  "type": "MultiPolygon",  "coordinates": [ [[[30, 20], [45, 40], [10, 40], [30, 20]]],  [[[15, 5], [40, 10], [10, 20], [5, 10], [15, 5]]] ] }, "address": {  "type": "Point", "coordinates": [-46.57421, -21.785741]}}' --request POST 'http://localhost:8000/api/v1/partners/'` |

---
#### Get a partner by Id
Get a partner given an Id.
| Field | Description  |
|--|--|
| URL | [/api/v1/partners/:id/](http://localhost:8000/api/v1/partners/1/) |
| Method | `GET` |
| URL Params | **Required** <br> `id=[int]` <br><br> **Optional** <br> None |
| Data Params | None |
| Samples Call | `curl --request GET 'http://localhost:8000/api/v1/partners/1/'` |

---
#### Get nearest partner by coordinate
Get a partner given a coordinate.
| Field | Description  |
|--|--|
| URL | [/api/v1/partners/:latitude/:longitude/](http://localhost:8000/api/v1/parters/-43.297337,-23.013538/) |
| Method | `GET` |
| URL Params | **Required** <br> `latitude=[float]`<br>`longitude=[float]` <br><br> **Optional** <br> None |
| Data Params | None |
| Samples Call | `curl --request GET 'http://localhost:8000/api/v1/partners/-43.297337,-23.013538/'` |
---

#### Partners List
List all partners given a page number.
| Field | Description  |
|--|--|
| URL | [/api/v1/partners/](http://localhost:8000/api/v1/partners/) |
| Method | `GET` |
| URL Params | **Required** <br> None <br><br> **Optional** <br>`page=[int]` <br><br> **Example** <br> `/api/v1/partners/?page=2`|
| Data Params | None |
| Samples Call | `curl --request GET 'http://localhost:8000/api/v1/partners/'` |
---

##  Instalation
### Via Docker
For this installation way, we are assuming yout have [Docker-compose](https://docs.docker.com/compose/install/) installed.

#### Step by Step
Go to server folder

    cd server

Build the project

    make build

Start the containers

    make up

Create all the tables of the database

    make migration

Populate the database with initial data

    make loaddata

Create a superuser

    make superuser

Then, open the browser in [localhost:8000/api/v1/partners/](http://localhost:8000/api/v1/partners/)

## Testing
If you are using Compose, run the tests with

    make test





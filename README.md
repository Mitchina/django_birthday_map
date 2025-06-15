#  Django Birthday Map
#### A collaborative platform that maps and showcases Django-related events happening worldwide.

It all started as a celebration of the Django birthday, inspiring the creation of a Django-themed map to track Python
and Django events globally. The project aims to foster connection and engagement across the Django community.

By combining geospatial technology with community participation, **Django Birthday Map** empowers developers and
enthusiasts to:

- Find and add events near them,
- Contribute to the growing map of Django happenings,
- Celebrate the global spirit of collaboration and learning.


## Table of Contents
- [Prerequisites](#prerequisites)
- [Quickstart](#quickstart)
  - [Clone](#clone)
  - [Project Dependencies](#project-dependencies)
  - [Environment Variables](#environment-variables)
  - [Spatial Database](#spatial-database)
  - [Testing Setup](#testing-setup)
  - [Database Migrations](#database-migrations)
  - [Load Events Data](#load-events-data)
  - [Create Superuser](#create-superuser)
  - [Run Server](#run-server)
- [Application](#application)


## Prerequisites

- Python 3.13.2
- pip (Python package installer)
- virtualenv or venv (optional but recommended)
- System libraries:
  - `libgdal-dev`, `gdal-bin` (Geospatial libraries)
  - `libpq5` (PostgreSQL client library)

## Quickstart

1. [Clone](#clone) the project code
2. Install the project [dependencies](#project-dependencies)
3. Set all the required [environment variables](#environment-variables)
4. Create a [spatial database](#spatial-database) (and add PostgreSQL PostGIS extension)
5. Add PostgreSQL PostGIS extension for [testing setup](#testing-setup) (optional)
6. Apply [database migrations](#database-migrations)
7. Load initial [events data](#events-data) fixture
8. [Create](#create-superuser) a superuser to login the platform
9. [Run](#run) the server
10. The [application](#application) will be running in DEBUG mode, at the URL: http://localhost:8000


### Clone

Clone the project locally:

```console
git clone git@github.com:Mitchina/django_birthday_map.git
cd django_birthday_map
```

### Project dependencies

Create and activate your virtual environment, then install dependencies:
```console
pip install -r requirements.txt
```

If you haven't installed system libraries yet, run:
```console
sudo apt install libgdal-dev gdal-bin libpq5
```

More info:
- https://pypi.org/project/GDAL/
- https://mothergeo-py.readthedocs.io/en/latest/development/how-to/gdal-ubuntu-pkg.html
- https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/postgis/


### Environment variables

Copy the example environment file:
```console
$ cp .env_template .env
```

Edit `.env` to set your database credentials and other settings.


### Spatial Database

Create the database and enable PostGIS extension:
```console
createdb -U postgres django_birthday_map
psql -U postgres django_birthday_map
CREATE EXTENSION postgis;
```

(The database user must be a superuser in order to run CREATE EXTENSION postgis;)


Create a database user and grant privileges:
```console
CREATE USER geodjango WITH PASSWORD 'password';
GRANT ALL PRIVILEGES ON DATABASE django_birthday_map TO geodjango;
ALTER DATABASE django_birthday_map OWNER TO geodjango;
```

Exit the shell:
```console
\q
```

See https://docs.djangoproject.com/en/5.2/ref/contrib/gis/install/postgis/#post-installation for details.


### Testing Setup (Optional)

To run tests involving PostGIS, enable PostGIS in the template database:
```console
sudo -u postgres psql -d template1 -c "CREATE EXTENSION IF NOT EXISTS postgis;"
```


### Database Migrations

Apply migrations:
```console
python manage.py migrate
```


### Load Events Data

Load initial events fixture:
```
python manage.py loaddata events/fixtures/events.json
```


### Create Superuser

Create a superuser for admin access:
```
$ python manage.py createsuperuser
```


### Run Server

Start the development server:
```console
python manage.py runserver
```

___
## Application
The application runs in DEBUG mode at [http://localhost:8000](http://localhost:8000).

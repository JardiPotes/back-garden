# Back-Garden

Back-Garden is the backend application for our JardiPotes project, a web app where people can book gardens to enjoy joyful moments with hosts.

## Setting up the project:

All dependencies of this project are dealt by poetry.
The database is on a Docker image, so you'll need to install Docker.
In order to retrieve all necessary dependencies, you need to:

- Install poetry: https://python-poetry.org/docs/#installation
- Create your `.env` file with POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD

### How to run the prorject?

Once you've cloned this repository and are ready to get your feet wet, you need to follow these steps to be able to run the app correctly.

- Activate the dev environment: `poetry shell`
- Install all dependencies: `poetry install`
- In a new terminal, launch the database: `docker-compose up -d`

#### Interacting with database

As all Django apps, everytime when you make a change on model files, you need to run these commands:

- `python manage.py makemigrations`
- `python manage.py migrate`

This includes token implementation as well.

#### How to run tests?

`poetry run python manage.py test`

#### How to launch the server?

`python manage.py runserver`

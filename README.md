# Back-Garden

Back-Garden is the backend application for our JardiPotes project, a web app where people can book gardens to enjoy joyful moments with hosts.

## Setting up the project:

All dependencies of this project are dealt by poetry.
The database is on a Docker image, so you'll need to install Docker.
In order to retrieve all necessary dependencies, you need to:

- Install poetry: https://python-poetry.org/docs/#installation
- Create your `.env` file with POSTGRES_DB, POSTGRES_USER, and POSTGRES_PASSWORD

## How to run the prorject?

Once you've cloned this repository and are ready to get your feet wet, you need to follow these steps to be able to run the app correctly.

- Activate the dev environment: `poetry shell`
- Install all dependencies: `poetry install`
- In a new terminal, launch the database: `docker-compose up -d db` (make sure your .env DB_HOST is set to "localhost")

### Interacting with database

As all Django apps, everytime when you make a change on model files, you need to run these commands:

- `python manage.py makemigrations`
- `python manage.py migrate`

This includes token implementation as well.

### How to run tests?

`poetry run python manage.py test`

### How to launch the server?

`python manage.py runserver`

### How to use pre-commit
Pre-commit checks run automatically. You may need to run `pre-commit` install the first time.

You can run all the checks manually by running `pre-commit run --all-files` in the terminal.

### Launch the app in a docker container
You can also launch the django app along with the database by running `docker-compose up -d` (.env.example DB_HOST must be set on "db")*<br>
The app will be accessible on `localhost:8000`.<br>
**improvements to come -.-*

### Deployment on Ada Tech School's server
`ssh debian@IP_DU_SERVEUR`
<br>enter password

(`ls`) > `cd back-garden` > `git pull` > `docker-compose up`

You might get an error if the db schema is not up-to-date

To run a command inside the container:
`docker ps` > c/c the container's id > `docker exec -it CONTAINER_ID bash`

(TODO: give a fixed name to the app container + run makemigrations & migrate on docker launch)

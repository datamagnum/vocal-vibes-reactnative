# VocalVibe Backend
This is a GitHub repo that houses the VovalVibe backend API, it is written with FastAPI

# Setup

## Pre-requisites:
1. Install [docker desktop](https://docs.docker.com/desktop/install/mac-install/)
2. Install [poetry](https://python-poetry.org/) if you have not already done so or run `pip install poetry==1.8.2`
3. Please use **python version 3.11** for this repository, it is recommended to use pyenv, [here](https://realpython.com/intro-to-pyenv/) is a very good setup guide. Other versions of python might result in issues when running certain scripts or downloading packages.
4. Once poetry is installed, run `poetry config virtualenvs.in-project true` , this will create the python virtual environment in the project repo itself, in a `.venv` folder 


## How to run locally:

1. `cd` into the project directory
2. Run `poetry shell` to enter the poetry shell
3. Run `poetry update` to update the virtual environment, if it's your first time running it, poetry will just install everything
4. Run `pre-commit init`  Run For first setup 
5. Run `docker compose up -d` to start the postgres vector database locally. Note: to stop the database gracefully, run `docker compose down`
6. Run `poetry run task app` to start the dev server


## Creating and migrating database:
1. At the root of the project, run `python /migrations/create_database.py` to create the local database. Your database docker container should already be running
2. To run the database migrations, run `alembic upgrade head`



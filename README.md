# Darapi

## Quickstart

### Run the app in containers

* Clone the repo and navigate to the root folder.

* To run the app using Docker, make sure you've got [Docker](https://www.docker.com/) and [Docker Compose V2](https://docs.docker.com/compose/cli-command/) installed on your system. From the project's root dirctory, to run the full setup with traefik proxy execute:

    ```bash
    docker compose up -d
    ```

* For development we also included a db-only docker-compose file, which can be executed via

    ```bash
    docker compose -f docker-compose.db-only.yml up -d
    ```

### Or, run the app locally

If you want to run the app locally, without using Docker, then:

* Clone the repo and navigate to the root folder.

* Create a virtual environment. Here I'm using Python's built-in venv in a Unix system. Run:

    ```bash
    python3.10 -m venv .venv
    ```

* Activate the environment. Run:

    ```bash
    source .venv/bin/activate
    ```

* Go to the folder created by cookie-cutter (default is **fastapi-nano**).

* Install the dependencies. Run:

    ```bash
    pip install -r requirements.txt && pip install -r requirements-dev.txt
    ```

* Start the app. Run:

    ```bash
    uvicorn app.main:app --port 5000 --reload
    ```

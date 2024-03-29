# DARA-API

This is a process repository containing and exposing [DARPAL](https://github.com/DaSKITA/darpal) specifications for well-established service providers.
To access the currently running API and see some example documents, please click [here](https://v2202301191442214869.powersrv.de/docs#/darpal/get_item_multi_darpal__get).

The Data Access Request Assistant (DARA) consists of 
* this process repository (DARA-API), 
* a browser-extension as automation engine ([DARA-Extension](https://github.com/DaSKITA/dara-extension)), and 
* a frontend ([DARA-Frontend](https://github.com/DaSKITA/dara-frontend))

As a starting point, we provide 15 DARPAL specifications, both in a running API [here](https://v2202301191442214869.powersrv.de/docs#/darpal/get_item_multi_darpal__get) and via a [github repository](https://github.com/DaSKITA/darpal-documents).


This process repository is based on FastAPI.
In the following, we kept the original FastAPI readme.

## Quickstart

### Run the app in containers

* Clone the repo and navigate to the root folder.

* Set the necessary enviroment variables as seen in `.env-example`. You can use the contents of the file as base for your local `.env`.

* To run the app using Docker, make sure you've got [Docker](https://www.docker.com/) and [Docker Compose V2](https://docs.docker.com/compose/cli-command/) installed on your system. From the project's root dirctory, to run the full setup with traefik proxy execute:

    ```bash
    docker compose up -d
    ```

### Or, run the app locally

If you want to run the app locally, without using Docker, then:

* Clone the repo and navigate to the root folder.

* Create a virtual environment. Here I'm using Python's built-in venv in a Unix system. Run:

    ```bash
    python -m venv .venv
    ```

* Activate the environment. Run:

    ```bash
    source .venv/bin/activate
    ```

* Install the dependencies. Run:

    ```bash
    pip install -r requirements.txt && pip install -r requirements-dev.txt
    ```

* Set the necessary enviroment variables as seen in [`.env-example`](./.env-example). You can use the contents of the file as base for your local `.env`.

* Start the db-only docker-compose file via:

    ```bash
    docker compose -f docker-compose.db-only.yml up -d
    ```

* Start the app. Run:

    ```bash
    uvicorn app.main:app --port 5000 --reload
    ```

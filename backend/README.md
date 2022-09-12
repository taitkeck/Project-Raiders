# springmicro-api

FastAPI server with JWT auth and Beanie ODM. Inspired by [fastapi-beanie-jwt](). Version 0.1, for development use only. For future versions and other updates, contact David Buckley.

## Features

- Registration
- Email verification
- Password reset
- JWT auth login and refresh
- User model CRUD

It's built on top of these libraries to provide those features:

- [FastAPI]() - Python async micro framework built on [Starlette]() and [PyDantic]()
- [Beanie ODM]() - Async [MongoDB]() object-document mapper built on [PyDantic]()
- [fastapi-jwt-auth]() - JWT auth for [FastAPI]()
- [fastapi-mail]() - Mail server manager for [FastAPI]()

## Setup

This codebase was written for Python 3.9 and above. Don't forget about a venv as well. The `python` commands below assume you're pointing to your desired Python3 target.

### Setup Virtual Env and Install Requirements

Think of a Python virtual environment like project-specific `node_modules`, and `requirements.txt` like the `package.json` dependencies.

```bash
# create a virtual environment directory called 'env'
python -m venv env
# use this environment in this terminal session (run source env/Scripts/activate if you're on Windows)
# you will need to do this every time you install something or run the backend project
source env/bin/activate
# install requirements
python -m pip install -r requirements.txt
```

### Environment Variables

Create the `.env` file by copying the example file.

```
cp .env.example .env
```

There is one config variable you'll need to generate the password salt. To do this, just run the script in this repo.

```bash
python gen_salt.py
```

There are other settings in `config.py` and the included `.env` file. Assuming you've changed the SALT value, everything should run as-is if there is a local [MongoDB]() instance running. Any email links will be printed to the console by default.

### MongoDB

Choose between the two options:

1. Run [MongoDB locally](). If you do this, you won't need to change the `.env` because that is the default.
2. Create an [MongoDB Free Tier Atlas cluster](). After creating your cluster, set the following variables in `.env` (replacing the current values with your cluster's values):

```
MONGO_URI="mongodb://localhost:27017"
DB_NAME="smapi"
```

## Run

This app uses [uvicorn]() as our ASGI web server. This allows us to run our server code in a much more robust and configurable environment than the development server. For example, ASGI servers let you run multiple workers that recycle themselves after a set amount of time or number of requests.

```bash
uvicorn sm_api.main:app --reload --port 8080
```

Your API should now be available at http://localhost:8080

The interactive API Docs are avaiable at http://localhost:8080/docs

## API Key for Frontend

When you run the backend server, an API Key is generated for your frontend to connect. Every model in the backend has a relation to the frontend app that connects to it. This is so multiple frontends can connect to the same API while each only having access to their app's data.

This API Key is located in `default_app.json`, which should have been generated the first time your run the server.

## Generate Fake Product Data

If you are supporting a shopping cart, you many want some fake product data to fill your database with. The `num_of_products` arg below is the integer number of products you would like to generate. This is done inefficiently, one product at a time, with no bulk product create, so keep your generation under 100 at a time.

> Make sure your server is running when you generate products in order for them to be stored in the database.

```
cd fake_data
python products.py <num_of_products:int>
```

[mongodb]: https://www.mongodb.com "MongoDB NoSQL homepage"
[fastapi]: https://fastapi.tiangolo.com "FastAPI web framework"
[beanie odm]: https://roman-right.github.io/beanie/ "Beanie object-document mapper"
[starlette]: https://www.starlette.io "Starlette web framework"
[pydantic]: https://pydantic-docs.helpmanual.io "PyDantic model validation"
[fastapi-jwt-auth]: https://github.com/IndominusByte/fastapi-jwt-auth "JWT auth for FastAPI"
[fastapi-mail]: https://github.com/sabuhish/fastapi-mail "FastAPI mail server"
[uvicorn]: https://www.uvicorn.org "Uvicorn ASGI web server"
[fastapi-beanie-jwt]: https://github.com/flyinactor91/fastapi-beanie-jwt "FastAPI with Beanie and JWT"
[mongodb locally]: https://www.mongodb.com/docs/manual/administration/install-community/ "Setup MongoDB Locally"
[mongodb free tier atlas cluster]: https://www.mongodb.com/docs/atlas/getting-started/ "Get Started with Atlas"

# BoltApp

Python Flask app for the ingestion and serving of data concerning various fasteners sold by various sellers.

# Setup

The following is to be run from the Boltwise folder, one higher up than the bolt_app folder.

## Install dependencies

`python3.12 -m venv .venv`
`. .venv/bin/activate`
`pip install -r requirements.txt`
If developing or debugging, run:
`pip install -r requirements.dev.txt`

## Run app

`python -m bolt_app.app`

# Testing

Using Postman one can make a GET request to the following URL (assuming still running locally with default settings): `http://127.0.0.1:5000/fasteners`

The equivalent `curl` command would be:
`curl --location 'http://127.0.0.1:5000/fasteners'`

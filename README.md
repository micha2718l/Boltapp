# BoltApp

Python Flask app for the ingestion and serving of data concerning various fasteners sold by various sellers.

# Setup

The following is to be run from the Boltwise folder, one higher up than the bolt_app folder.

## Install dependencies

```
python3.10 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
```

If developing or debugging, run:

`pip install -r requirements.dev.txt`

# Operation

## Run app

`python -m bolt_app.app`

## Ingest data

`flask --app bolt_app commands ingest FILENAME`

This command will read in the file given and parse it for a seller name and the data contained. If it is seller 'a' or seller 'b', the parsing will be handed off to the appropriate handler and parsed accordingly. Otherwise it will fail silently.

This command performs upserts on the dual consstraint of 'seller' and 'external_sku'. Therefore, each seller may have one each of unique product id that will then be updated with subsequent runs.

# Testing

Using Postman one can make a GET request to the following URL (assuming still running locally with default settings):
`http://127.0.0.1:5000/fasteners`

A query parameter of `sort` can be included which indicates the field to sort by as well as optionally the order, separated by a colon as below:

`http://127.0.0.1:5000/fasteners?sort=thread_size:desc`

The default sort is by category in an ascending order.

The equivalent `curl` command would be:
`curl --location 'http://127.0.0.1:5000/fasteners'`

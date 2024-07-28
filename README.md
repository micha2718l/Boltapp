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

# Current Deployment

There is a current "production" deploy of this code which has has the 3 "migration" files run against it.
This app is currently deployed on PythonAnywhere with use of their hosted mySQL db service at the address:

`https://boltapp.pythonanywhere.com/`

This is the command output of running the migrations:

```
(.venv) 21:47 ~/Boltwise (main)$ flask --app bolt_app commands ingest sample_data/seller-a-20240625-csv-updated.csv
Ingesting sample_data/seller-a-20240625-csv-updated.csv
0
/home/boltapp/Boltwise/bolt_app/utils.py:86: SAWarning: Object of type <Fastener> not in session, add operation along 'Seller.fasteners' will not proceed
  db.session.commit()
1
2
3
4
(.venv) 21:49 ~/Boltwise (main)$ flask --app bolt_app commands ingest sample_data/seller-b-20240625-csv-updated.csv
Ingesting sample_data/seller-b-20240625-csv-updated.csv
0
/home/boltapp/Boltwise/bolt_app/utils.py:86: SAWarning: Object of type <Fastener> not in session, add operation along 'Seller.fasteners' will not proceed
  db.session.commit()
1
2
3
4
(.venv) 21:49 ~/Boltwise (main)$ flask --app bolt_app commands ingest sample_data/seller-a-20240727-csv-updated.csv
Ingesting sample_data/seller-a-20240727-csv-updated.csv
0
/home/boltapp/Boltwise/bolt_app/utils.py:86: SAWarning: Object of type <Fastener> not in session, add operation along 'Seller.fasteners' will not proceed
  db.session.commit()
1
2
3
4
5
(.venv) 21:49 ~/Boltwise (main)$
```

This allows requests like:

`https://boltapp.pythonanywhere.com/fasteners?sort=finish:asc`

Sample output from request:
GET `https://boltapp.pythonanywhere.com/fasteners?sort=finish:asc`:
RESPONSE

```
[
  {
    "category": "Hex Cap Screw",
    "finish": "Plain",
    "id": 1,
    "material": "Steel",
    "seller": {
      "id": 1,
      "name": "a"
    },
    "thread_size": "M10-1.5"
  },
  {
    "category": "Hex Cap Screw",
    "finish": "Plain",
    "id": 3,
    "material": "Steel",
    "seller": {
      "id": 1,
      "name": "a"
    },
    "thread_size": "M12-1.75"
  },
  {
    "category": "Hex Cap Screw",
    "finish": "Teflon Blue",
    "id": 2,
    "material": "Steel",
    "seller": {
      "id": 1,
      "name": "a"
    },
    "thread_size": "1/4-20"
  },
  {
    "category": "Hex Cap Screw",
    "finish": "Zinc",
    "id": 4,
    "material": "Steel",
    "seller": {
      "id": 1,
      "name": "a"
    },
    "thread_size": "M14-2"
  },
  {
    "category": "Hex Cap Screw",
    "finish": "Zinc",
    "id": 5,
    "material": "Steel",
    "seller": {
      "id": 1,
      "name": "a"
    },
    "thread_size": "M8-1.25"
  }
]
```

# Data Analysis

There is a Jupyter notebook in this folder called `exploratory_analysis.ipynb` where one may see how the initial analysis of csv data was done. This was done using pandas to ensure that future exploratory work is easy to accomplish.

# QuickQuick

[![code-style](https://github.com/r0mainK/quickquick/actions/workflows/code-style.yml/badge.svg)](https://github.com/r0mainK/quickquick/actions/workflows/code-style.yml)

Minimal URL shortening service.
The frontend has a touch of JS and CSS but nothing too fancy.
The backend is made in Python, with the help of a couple packages: FastAPI, SQLAlchemy and Pydantic.
The database is SQLite.

## Usage

### Via Docker

```
docker build -t quickquick .
docker run --rm -p 80:80 quickquick
```

Note that:

- a volume will persist the Database, it is mounted to `/opt/db`
- you can run the container in the background using "detached" mode
- you can enable the documentation endpoints by overriding the `DISABLE_DOCUMENTATION` environment variable

### Via a virtual environment

You will need:

- Python 3.10 (higher probably works)
- Poetry 1.6.1 (higher probably works)

```
poetry run uvicorn quickquick.server:app --reload
```

Note that the location of the DB can be set using the `SQLITE_FILEPATH` environment variable.

## Dev

### Tests

There are none - for now ?

### Style

Powered by pre-commit.

### Minify JS

Because why not:

```
terser quickquick/static/script.js -c -m -o quickquick/static/script.min.js
sed -i 's/script.js/script.min.js/g' quickquick/static/index.html
```

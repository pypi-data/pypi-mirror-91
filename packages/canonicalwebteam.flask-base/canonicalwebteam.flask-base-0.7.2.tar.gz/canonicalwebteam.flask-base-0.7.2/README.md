# Canonical Webteam Flask-Base

Flask extension that applies common configurations to all of webteam's flask apps.

## Usage

```python3
from canonicalwebteam.flask_base.app import FlaskBase

app = FlaskBase(__name__, "app.name")
```

Or:

```python3
from canonicalwebteam.flask_base.app import FlaskBase

app = FlaskBase(
    __name__,
    "app.name",
    template_404="404.html",
    template_500="500.html",
    favicon_url="/static/favicon.ico",
)
```

## Features

### Redirects and deleted paths

FlaskBase uses [yaml-responses](https://github.com/canonical-web-and-design/canonicalwebteam.yaml-responses) to allow easy configuration of redirects and return of deleted responses, by creating `redirects.yaml`, `permanent-redirects.yaml` and `deleted.yaml` in the site root directory.

### Error templates

`FlaskBase` can optionally use templates to generate the `404` and `500` error responses:

```python3
app = FlaskBase(
    __name__,
    "app.name",
    template_404="404.html",
    template_500="500.html",
)
```

This will lead to e.g. `http://localhost/non-existent-path` returning a `404` status with the contents of `templates/404.html`.

### Redirect /favicon.ico

`FlaskBase` can optionally provide redirects for the commonly queried paths `/favicon.ico`, `/robots.txt` and `/humans.txt` to sensible locations:

```python3
from canonicalwebteam.flask_base.app import FlaskBase

app = FlaskBase(
    __name__,
    "app.name",
    template_404="404.html",
    template_500="500.html",
    favicon_url="/static/favicon.ico",
    robots_url="/static/robots.txt",
    humans_url="/static/humans.txt"
)
```

This will lead to e.g. `http://localhost/favicon.ico` returning a `302` redirect to `http://localhost/static/favicon.ico`.

### Jinja2 helpers

You get two jinja2 helpers to use in your templates from flask-base:

- `now` is a function that outputs the current date in the passed [format](https://docs.python.org/3/library/datetime.html#strftime-and-strptime-format-codes) - `{{ now('%Y') }}` -> `YYYY`
- `versioned_static` is a function that fingerprints the passed asset - `{{ versioned_static('asset.js') }}` -> `static/asset?v=asset-hash`

### `robots.txt` and `humans.txt`

If you create a `robots.txt` or `humans.txt` in the root of your project, these will be served at `/robots.txt` and `/humans.txt` respectively.

## Tests

To run the tests execute `SECRET_KEY=fake python3 -m unittest discover tests`.

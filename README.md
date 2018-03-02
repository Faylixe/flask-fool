# flask-fool

[![pypi](https://img.shields.io/pypi/v/flask-fool.svg)](https://pypi.python.org/pypi/Flask-Fool) [![CircleCI](https://circleci.com/gh/Faylixe/flask-fool.svg?style=shield)](https://circleci.com/gh/Faylixe/flask-fool)

A Flask extension that prevents browser access to API by faking browser error pages.

## Usage

```python
from flask import flask
from flask_fool import FlaskFool

app = Flask('myapp')
fooler = FlaskFool(app)
```

From now if any error is caught by the application and the query has been emitted by a browser,
an error page corresponding to the used browser will be returned, suggesting that the queried
domain does not exist.


## Disallow browser access

You can also totally prevent for browser access by using ``disallow_browser`` flag :

```python
fooler = FlaskFool(app, disallow_browser=True)
```

## User agent filtering

You can also just want your API only be reachable by a specific user agent. In that case you can
specify a custom user agent for which only request will be received :

```python
fooler = FlaskFool(app, user_agent='MyCustomUserAgent')
```

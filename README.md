# flask-fool

A Flask extension that prevents browser access to API by faking browser error pages.

## Usage

```python
from flask import flask
from flask.ext.flask_fool import FlaskFool

app = Flask('myapp')
fooler = FlaskFool(app)
```

From now if any error is caught by the application and the query has been emitted by a browser,
an error page corresponding to the used browser will be returned, suggesting that the queried
domain does not exist.

## User agent filtering

You can also just want your API never been reached by a web browser. In that case you can
specify a custom user agent for which only request will be received :

```python
from flask import flask
from flask.ext.flask_fool import FlaskFool

app = Flask('myapp')
fooler = FlaskFool(app, agent='MyCustomUserAgent')
```

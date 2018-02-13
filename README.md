# flask-fool

A Flask extension that prevents browser access to application by faking browser error pages.

## Usage

```python
from flask import flask
from flask.ext.flask_fool import FlaskFool

app = Flask('myapp')

def _create_json_error(exception):
    response = jsonify(message=str(exception))
    response.status_code = 500
    if isinstance(exception, HTTPException):
        if exception.code == 404:
            return send_from_directory('static', 'chrome.html')
        response.status_code = exception.code
    return response

FlaskFool()
#!/usr/bin/env python
# coding: utf8

""" Flask fool extension provide API hiding trick for JSON web services. """

from flask import request, render_template
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

__author__ = 'fv'
__version__ = '1.0.0'



def _is_browser():
    """ Simple predicate function that check if the user agent
    denoted a supported browser or not.

    :returns: True if request has been emitted from a browser, False otherwise.
    """
    return request.user_agent.browser in ['firefox', 'chrome']


def _deny_browser():
    """ Deny the browser usage of this request.

    :returns: Error page response.
    """
    browser = request.user_agent.browser
    hostname = request.remote_addr
    if browser == 'firefox':
        return render_tempate('firefox.html', hostname=hostname), 404
    return render_tempate('chrome.html', hostname=hostname), 404


class FlaskFool(object):
    """ The request proxy fooler :). """

    def __init__(self, application=None, user_agent=None):
        """ Default constructor.

        :param application: (Optional)
        :param user_agent: (Optional)
        """
        self._user_agent = user_agent
        if application is not None:
            self.init_app(application)

    def init_app(self, application):
        """ Extension initializer method. Configures the given
        application with this extension by adding the request
        proxy method as before handler.

        :param application: Application to configure.
        """
        self._application = application
        for code in default_exceptions:
            self._application.register_error_handler(code, self._on_error)
        if self._user_agent is not None:
            self._application.before_request(self._on_request)

    def _on_error(self, exception):
        """ Custom error handler method used to generate
        JSON error message for the given exception.

        :param exception: Exception to transform.
        :returns: Transformed exception into a JSON error response.
        """
        if _is_browser():
            return _deny_browser()
        response = jsonify(message=str(exception))
        response.status_code = 500
        if isinstance(exception, HTTPException):
            response.status_code = exception.code
        return response

    def _on_request(self):
        """ The concrete request proxy method that allows
        request execution regarding of the provided user agent.

        :returns: An error page based on the browser (eventually).
        """
        if request.user_agent.string != self._user_agent:
            return _deny_browser()

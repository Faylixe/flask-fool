#!/usr/bin/env python
# coding: utf8

""" Flask fool extension provide API hiding trick for JSON web services. """

from flask import jsonify, request, render_template
from jinja2 import ChoiceLoader, PackageLoader
from werkzeug.exceptions import default_exceptions
from werkzeug.exceptions import HTTPException

__author__ = 'fv'


def _is_browser():
    """ Simple predicate function that check if the user agent
    denoted a supported browser or not.

    :returns: True if request has been emitted from a browser, False otherwise.
    """
    # TODO : Handle more browser.
    return request.user_agent.browser in ['firefox', 'chrome']


class FlaskFool(object):
    """ The request proxy fooler :). """

    def __init__(
            self,
            application=None,
            disallow_browser=False,
            user_agent=None):
        """ Default constructor.

        :param application: (Optional) Target flask application.
        :param disallow_browser: (Optional) Indicates if browser is supported.
        :param user_agent: (Optional) User agent allowed.
        """
        self._disallow_browser = disallow_browser
        self._user_agent = user_agent
        self._hostname = None
        if application is not None:
            self.init_app(application)

    def init_app(self, application):
        """ Extension initializer method. Configures the given
        application with this extension by adding the request
        proxy method as before handler.

        :param application: Application to configure.
        """
        self._application = application
        if 'HOST' in application.config:
            self._hostname = application.config['HOST']
        loader = ChoiceLoader([
            PackageLoader('flask_fool'),
            self._application.jinja_loader
        ])
        self._application.jinja_loader = loader
        for code in default_exceptions:
            self._application.register_error_handler(code, self._on_error)
        filter_all = any([
            self._user_agent is not None,
            self._disallow_browser
        ])
        if filter_all:
            self._application.before_request(self._on_request)

    def _deny(self):
        """ Deny the usage of this request.

        :returns: Error page response.
        """
        browser = request.user_agent.browser
        hostname = request.remote_addr
        if self._hostname is not None:
            hostname = self._hostname
        if browser == 'firefox':
            return render_template('firefox.html', hostname=hostname), 404
        if browser == 'chrome':
            return render_template('chrome.html', hostname=hostname), 404
        # TODO : Handle default browser page.
        return render_tempate('chrome.html', hostname=hostname), 404

    def _on_error(self, exception):
        """ Custom error handler method used to generate
        JSON error message for the given exception.

        :param exception: Exception to transform.
        :returns: Transformed exception into a JSON error response.
        """
        if _is_browser():
            return self._deny()
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
        if self._disallow_browser:
            return self._deny()
        if request.user_agent.string != self._user_agent:
            return self._deny()

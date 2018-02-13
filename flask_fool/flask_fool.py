#!/usr/bin/env python
# coding: utf8

""" """

from flask import request, render_template

__author__ = 'fv'
__version__ = '1.0.0'


class FlaskFool(object):
    """ The request proxy fooler :). """

    def __init__(self, application=None):
        """ Default constructor.

        :param application: (Optional)
        """
        self._allowed_agents = []
        if application is not None:
            self.init_app(application)

    def add_agent(self, agent):
        """ Adds the given agent as allowed to query the application.

        :param agent: Agent to allow.
        """
        self._allowed_agents.append(agent)

    def init_app(self, application):
        """ Extension initializer method. Configures the given
        application with this extension by adding the request
        proxy method as before handler.

        :param application: Application to configure.
        """
        self._application = application
        self._application.before_request(self._on_request)

    def _on_request(self):
        """ The concrete request proxy method that allows
        request execution regarding of the provided user agent.

        :returns: An error page based on the browser (eventually).
        """
        user_agent = request.user_agent
        if user_agent.string not in self._allowed_agents:
            browser = user_agent.browser
            hostname = request.remote_addr
            if browser == 'firefox':
                return render_tempate('firefox.html', hostname=hostname), 404
            elif browser == 'chrome':
                return render_tempate('chrome.html', hostname=hostname), 404
            # TODO : Add other browser support.

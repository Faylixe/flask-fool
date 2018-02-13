#!/usr/bin/env python
# coding: utf8

""" Test extension. """

from flask import Flask
from pytest import fixture
from requests import get

from flask_fool.flask_fool import FlaskFool

__author__ = 'fv'
__version__ = '1.0.0'

_ALLOWED = 'MyCustomUserAgent'
_CHROME = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
_FIREFOX = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'


@fixture
def client():
    """ Simple extension fixture. """
    def _view():
        return 'OK', 200
    application = Flask('test-application')
    application.add_url_rule('/', 'page', view_func=_view)
    extension = FlaskFool()
    extension.init_app(application)
    extension.add_agent(_ALLOWED)
    return application.test_client()


def test_allowed_agent(client):
    """ Test successful request. """
    response = client.get('/', headers={'User-Agent': _ALLOWED})
    assert response.status_code == 200
    assert response.data =='OK'


def test_chrome_agent(client):
    """ Test unallowed with chrome user agent. """
    response = client.get('/', headers={'User-Agent': _CHROME})
    assert response.status_code == 404
    # TODO : Check response content.


def test_firefox_agent(client):
    """ Test unallowed with firefox user agent. """
    response = client.get('/', headers={'User-Agent': _FIREFOX})
    assert response.status_code == 404
    # TODO : Check response content.

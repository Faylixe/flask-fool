#!/usr/bin/env python
# coding: utf8

""" Test extension. """

from flask import Flask
from pytest import fixture
from requests import get

from flask_fool import FlaskFool

__author__ = 'fv'
__version__ = '1.0.0'

_ALLOWED = 'MyCustomUserAgent'
_CHROME = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36'
_FIREFOX = 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1'


@fixture
def application():
    """ Flask application fixture. """
    def _view():
        return 'OK', 200
    application = Flask('test-application')
    application.testing = True
    application.add_url_rule('/', 'page', view_func=_view)
    return application


@fixture
def simple_client(application):
    """ Basic extension related client fixture. """
    FlaskFool(application)
    return application.test_client()


@fixture
def browser_forbidden_client(application):
    """ Browser forbidden extension related client fixture. """
    FlaskFool(application, True)
    return application.test_client()


@fixture
def user_agent_client(application):
    """ User agent filtering extension related client fixture. """
    FlaskFool(application, False, _ALLOWED)
    return application.test_client()


def _verify_success(client, user_agent):
    """ Performs a valid request and ensures result is successfull.

    :param client: Target client to use for request.
    :param user_agent: Target user agent to use for request.
    """
    response = client.get('/', headers={'User-Agent': user_agent})
    assert response.status_code == 200
    assert response.data == b'OK'


def _verify_failure(client, user_agent, url='/'):
    """ Performs a unvalid request and returns associated data.

    :param client: Target client to use for request.
    :param user_agent: Target user agent to use for request.
    :param url: Target unvalid url to request.
    :returns: Request associated response data.
    """
    response = client.get(url, headers={'User-Agent': user_agent})
    assert response.status_code == 404
    return response.data


def test_valid_request(simple_client):
    """ Test valid request without filtering. """
    _verify_success(simple_client, _FIREFOX)


def test_allowed_agent(user_agent_client):
    """ Test allowed agent. """
    _verify_success(user_agent_client, _ALLOWED)


def test_unallowed_agent(user_agent_client):
    """ Test unallowed user agent. """
    _verify_failure(user_agent_client, _CHROME)


def test_browser_forbidden(browser_forbidden_client):
    """ Test browser forbidden request."""
    _verify_failure(browser_forbidden_client, _CHROME)


def test_firefox_agent(simple_client):
    """ Test error with firefox user agent. """
    data = _verify_failure(simple_client, _FIREFOX, '/foo')
    # TODO : Check returned data.


def test_chrome_agent(simple_client):
    """ Test error with chrome user agent. """
    data = _verify_failure(simple_client, _CHROME, '/foo')
    # TODO : Check returned data.

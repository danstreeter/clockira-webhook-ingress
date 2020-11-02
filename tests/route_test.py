# System Imports
import pytest
from unittest import mock
from unittest.mock import MagicMock


# Framework / Library Imports

# Application Imports
from main import create_app
import config
# Local Imports

@mock.patch('comms_rabbitmq.get_connection')
def test_no_rootpatch(get_conn):
    """
    Tests that a blank route returns a 404
    """
    get_conn = MagicMock()
    get_conn.return_value = True
    get_conn.channel = MagicMock()

    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    rv = client.get('/')
    assert rv.status_code == 404

@mock.patch('comms_rabbitmq.get_connection')
def test_healthcheck(get_conn):
    """
    Tests that the healthcheck returns a 200
    and a text response of 'OK'
    """
    get_conn = MagicMock()
    get_conn.return_value = True
    get_conn.channel = MagicMock()

    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()
    rv = client.get('/healthcheck')
    assert rv.status_code == 200
    assert b"OK" in rv.data

@mock.patch('comms_rabbitmq.publish_webhook')
@mock.patch('comms_rabbitmq.get_connection')
def test_rmq_runs_webhook(get_conn, mocked_method):
    """
    Tests that when the config mode is RABBITMQ
    a publish_nats event is run
    """
    get_conn = MagicMock()
    get_conn.return_value = True
    get_conn.channel = MagicMock()

    mocked_method.return_value = True

    app = create_app()
    app.config['TESTING'] = True
    client = app.test_client()

    rv = client.post('/clockify/webhook/test')
    mocked_method.assert_called_once()

    assert rv.status_code == 200

# How to get Flask config
#    print(client.application.config)
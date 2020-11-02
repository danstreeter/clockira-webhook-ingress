"""Configuration module"""
# noqa
# System Imports

# Framework / Library Imports

# Application Imports

# Local Imports
import env_creds as creds

APP_VERSION = '0.0.1'
APP_DATE = '2020-11-02 1900'
APP_NODE = creds.APP_NODE

API_PREFIX = creds.API_PREFIX

DEBUG = creds.DEBUG

# RabbitMQ Queue Configuration
RABBITMQ = {
    "server": creds.RABBIT_SERVER,
    "port": creds.RABBIT_PORT,
    "user": creds.RABBIT_USER,
    "password": creds.RABBIT_PASS
}

"""
Module to handle specifically comminication actions with RabbitMQ
"""
# System Imports
import json
import os

# Framework / Library Imports
import pika

# Application Imports

# Local Imports
import config


def get_connection():
    """
    Returns a connection object for RabbitMQ
    """
    try:
        credentials = pika.PlainCredentials(config.RABBITMQ['user'], config.RABBITMQ['password'])
        rmq_connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=config.RABBITMQ['server'],
                port=config.RABBITMQ['port'],
                virtual_host='/',
                credentials=credentials,
                client_properties={
                    'connection_name': "Clockify Webhook Ingress Node: {}[{}]".format(
                        config.APP_NODE,
                        os.getpid()
                    )
                }
            )
        )
    except Exception as exc:
        error_string = "Unable to connect using {username}:{password}@{server}:{port}".format(
            username=config.RABBITMQ['user'],
            password=config.RABBITMQ['password'],
            server=config.RABBITMQ['server'],
            port=config.RABBITMQ['port']
        )
        print(error_string)
        raise ConnectionError('Connection Error: ' + error_string, status_code=500) from exc
    return rmq_connection


def publish_webhook(queue_payload, queue):
    """
    Publishes a webhook payload onto the inbound webhook queue for processing
    """
    conn = get_connection()
    channel = conn.channel()
    channel.basic_publish(
        exchange='',
        routing_key=queue,
        properties=pika.BasicProperties(
            content_type="application/json",
            headers={
                'task': queue_payload['task']
            }
        ),
        body=json.dumps(queue_payload))
    conn.close()
    return True


def create_queue_payload(req, task=None, payload_override=None):
    """
    Helper method to form the required queue payload from inbound object
    """
    return {
        "task": task or "clockify.webhook",
        "meta": {
            "headers": {
                str(header[0]): req.headers.get(str(header[0]), None) for header in req.headers
            } or None
        },
        "params": {str(arg): req.args.get(str(arg), None) for arg in req.args} or None,
        "payload": payload_override or req.json or None,
        "system": {
            "element": "clockify_webhook_ingress",
            "node": config.APP_NODE,
            "version": config.APP_VERSION,
            "version_date": config.APP_DATE
        }
    }

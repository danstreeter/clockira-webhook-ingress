# System Imports
import json

# Framework / Library Imports
from flask import abort, Flask, request

# Application Imports

# Local Imports


def create_app(config=None):
    if config is None:
        import config
    print(f"Starting HTTP Ingress v{config.APP_VERSION}")

    app = Flask(__name__)

    # RabbitMQ Bootstrap
    from comms_rabbitmq import get_connection, publish_webhook, create_queue_payload
    conn = get_connection()
    channel = conn.channel()
    channel.queue_declare("clockify.webhook.inbound", False, True)
    print(f"RMQ connected to {config.RABBITMQ['server']}:{config.RABBITMQ['port']}")

    @app.route(config.API_PREFIX + '/clockify/webhook/<event>', methods=['POST'])
    def respond(event):
        processed = False
        # Publish the job onto the queue
        publish_webhook(create_queue_payload(request, task=event), queue="clockify.webhook.inbound")
        processed = True

        if not processed:
            abort(500)
        else:
            return "Received"

    @app.route('/healthcheck', methods=['GET'])
    def healthcheck():
        return "OK"

    return app

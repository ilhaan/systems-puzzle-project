#!/usr/bin/env python
import pika
import json
import os
import time
import sys
from utils import parse_log, is_get_request

#Connect  to RabbitMQ
credentials = pika.PlainCredentials(os.environ['RABBITMQ_DEFAULT_USER'], os.environ['RABBITMQ_DEFAULT_PASS'])
parameters = pika.ConnectionParameters(host='rabbit',
                                       port=5672, credentials=credentials)

while True:
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.ConnectionClosed:
        print('Ingestion: RabbitMQ not up yet.')
        time.sleep(2)

print('Ingestion: Connection to RabbitMQ established')


# Start queue

channel = connection.channel()
channel.queue_declare(queue='log-analysis')

# Read weblogs

f = open('weblogs.log', 'r')

while True:
    try:
        msg = f.readline()

        if not msg:
            break
        #If message is GET request, ingest it into the queue
        if is_get_request(msg):
            # Parse GET request for relevant information
            day, status, source = parse_log(msg)

            # Store in RabbitMQ
            body = json.dumps({'day': str(day), 'status': status})
            channel.basic_publish(exchange='',
                                  routing_key='log-analysis',
                                  body=body)

    except:
        print("Unexpected error:" +  sys.exc_info()[0])

connection.close()

#!/usr/bin/env python
import pika
import time
import psycopg2
import os
import json

# Connect to RabbitMQ
credentials = pika.PlainCredentials(os.environ['RABBITMQ_DEFAULT_USER'], os.environ['RABBITMQ_DEFAULT_PASS'])
parameters = pika.ConnectionParameters(host='rabbit',
                                       port=5672, credentials=credentials)

while True:
    try:
        connection = pika.BlockingConnection(parameters)
        break
    except pika.exceptions.AMQPConnectionError:
        print('Processing: RabbitMQ not up yet.')
        time.sleep(2)
        
print('Processing: Connection to RabbitMQ established')

# Connect to log-analysis channgel
channel = connection.channel()
channel.queue_declare(queue='log-analysis')

# Connect to PostgreSQL database
conn = psycopg2.connect(host='db', database=os.environ['POSTGRES_DB'], user=os.environ['POSTGRES_USER'], password=os.environ['POSTGRES_PASSWORD'])
cur = conn.cursor()


# main function that reads from RabbitMQ queue and stores it in database
def callback(ch, method, properties, body):
    msg = json.loads(body)
    values = "to_date(\'" + msg['day'] + "\', \'YYYY-MM-DD\')" + ", " + '200'
    sql = """INSERT INTO weblogs (day, status)
             VALUES (%s);""" % values
    cur.execute(sql, body)
    conn.commit()
    
#Start consumer
channel.basic_consume(callback,
                      queue='log-analysis',
                      no_ack=True)

channel.start_consuming()

from confluent_kafka import Consumer, KafkaError, KafkaException

import sys
import json

kafkaIP = "10.30.2.118"
kafkaPort = 9092

#topic = "fgt-82f4710-3d04-429a-8243-5a2ac741fd4d_forecasting"
topic = "Test"
conf = {'bootstrap.servers': kafkaIP + ":" + str(kafkaPort),
        'group.id': 'mygroup',
        'auto.offset.reset': 'smallest'}

consumer = Consumer(conf)
'''
# Producer configuration
message = "test message"
consumer = Consumer({
    'bootstrap.servers': kafkaIP + ":" + str(kafkaPort),
    'group.id': 'mygroup',
    'auto.offset.reset': 'smallest'
})
consumer.subscribe([topic])

while True:
    print("test")
    try:
        print(consumer.list_topics())
        msg = consumer.poll(1.0)
        if msg is None:
            continue
        elif not msg.error():
            print('Received message: {0}'.format(msg.value()))
        elif msg.error().code() == KafkaError._PARTITION_EOF:
            print('End of partition reached {0}/{1}'
                  .format(msg.topic(), msg.partition()))
        else:
            print('Error occurred: {0}'.format(msg.error().str()))

    except KeyboardInterrupt as e:
        print("Consumer error: {}".format(str(e)))
        # Should be commits manually handled?
consumer.close()

'''


def dataParser(json_data):
    parsed_json = (json.loads(json_data))
    #print(json.dumps(parsed_json, indent=4, sort_keys=True))
    loaded_json = json.loads(json_data)
    for element in loaded_json:
        print("%s: %s" % (element['metric']['instance'], element['value'][1]))


running = True
try:
    consumer.subscribe([topic])

    while running:
        msg = consumer.poll(timeout=1.0)
        if msg is None: continue

        if msg.error():
            if msg.error().code() == KafkaError._PARTITION_EOF:
                # End of partition event
                sys.stderr.write('%% %s [%d] reached end at offset %d\n' %
                                 (msg.topic(), msg.partition(), msg.offset()))
            elif msg.error():
                raise KafkaException(msg.error())
        else:
            #print(msg)
            dataParser(msg.value())
finally:
    # Close down consumer to commit final offsets.
    consumer.close()

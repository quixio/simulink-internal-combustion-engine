import quixstreams as qx
import time
import datetime
import os
import random

client = qx.QuixStreamingClient()
topic_producer = client.get_topic_producer(topic_id_or_name = os.environ["output"])
stream = topic_producer.create_stream() 

#while True:
#    throttle_angle = random.uniform(8, 12)
#    data = qx.TimeseriesData()
#    data.add_timestamp(datetime.datetime.utcnow()) \
#        .add_value("throttle_angle", throttle_angle)
#    stream.timeseries.publish(data)
#    time.sleep(1)

for i in range(30):
    data = qx.TimeseriesData()
    data.add_timestamp(datetime.datetime.utcnow()) \
        .add_value("throttle_angle", i)
    stream.timeseries.publish(data)
    print("send angle: {}".format(i))
    time.sleep(1)

print("Done")
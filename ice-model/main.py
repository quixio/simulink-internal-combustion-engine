import quixstreams as qx
import os
import quixmatlab
import matlab

qxmlm = quixmatlab.initialize()

client = qx.QuixStreamingClient()
input_topic = client.get_topic_consumer(os.environ["input"])
output_topic = client.get_topic_producer(os.environ["output"])

def on_data_received_handler(input_stream: qx.StreamConsumer, data: qx.TimeseriesData):
    with data:
        for ts in data.timestamps:    
            throttle_angles = matlab.double([ts.parameters["throttle_angle"].numeric_value])
            timestamps = matlab.double([ts.timestamp_milliseconds / 1000])
            rv = qxmlm.engine(throttle_angles, timestamps)
            ts.add_value("engine_speed", rv)
            print("throttle angle:{}, engine speed:{}".format(throttle_angles[0][0], rv))
        output_stream = output_topic.get_or_create_stream(input_stream.stream_id)
        output_stream.timeseries.publish(data)

def on_stream_received_handler(stream: qx.StreamConsumer):
    print("New stream: {}".format(stream.stream_id))
    stream.timeseries.on_data_received = on_data_received_handler

input_topic.on_stream_received = on_stream_received_handler

print("Listening to streams. Press CTRL-C to exit.")
qx.App.run()
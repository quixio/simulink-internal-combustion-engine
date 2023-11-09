import quixstreams as qx
import os
import quixmatlab
import matlab
import time
import uuid

qxmlm = quixmatlab.initialize()

stream_id = str(uuid.uuid4())
client = qx.QuixStreamingClient()
input_topic = client.get_topic_consumer(os.environ["input"])
output_topic = client.get_topic_producer(os.environ["output"])
output_stream = output_topic.get_or_create_stream(stream_id)
#output_stream.timeseries.buffer.time_span_in_milliseconds = int(os.environ["buffer_ms"])

def on_data_recv_handler(sc: qx.StreamConsumer, data: qx.TimeseriesData):
    with data:
        t = []
        theta = []
        kv = []
        for ts in data.timestamps:    
            k = ts.timestamp_nanoseconds
            v = ts.parameters["throttle_angle"].numeric_value
            t.append(ts.timestamp_milliseconds / 1000.0)
            theta.append(v)
            kv.append((k, v))
            
        throttle_profile = matlab.double(theta)
        timeseries = matlab.double(t)
        try:
            t0 = time.time()
            rv = qxmlm.engine(throttle_profile, timeseries)
            t1 = time.time()
            print("time taken = {} seconds".format(t1 - t0))

            i = 0
            data_out = qx.TimeseriesData()
            for ts in rv:
                nanos = int(ts[0] * 1000000000)
                while i < len(kv) and kv[i][0] < nanos:
                    data_out.add_timestamp_nanoseconds(kv[i][0]) \
                            .add_value("throttle_angle", kv[i][1])
                    output_stream.timeseries.buffer.publish(data_out)
                    print("time={}, theta={}".format(kv[i][0], kv[i][1]))
                    i += 1

                output_stream.timeseries.buffer.flush()
                output_stream.timeseries.buffer \
                    .add_timestamp_nanoseconds(nanos) \
                    .add_value("v_engine", float(ts[1])) \
                    .publish()
                print("time={}, speed={}".format(nanos, ts[1]))
            output_stream.timeseries.buffer.flush()
        except Exception as e:
            print(e)

def on_stream_recv_handler(stream: qx.StreamConsumer):
    print("New stream: {}".format(stream.stream_id))
    buf = stream.timeseries.create_buffer()
    buf.time_span_in_milliseconds = int(os.environ["buffer_ms"])
    buf.on_data_released = on_data_recv_handler

input_topic.on_stream_received = on_stream_recv_handler

print("Listening to streams. Press CTRL-C to exit.")
qx.App.run()
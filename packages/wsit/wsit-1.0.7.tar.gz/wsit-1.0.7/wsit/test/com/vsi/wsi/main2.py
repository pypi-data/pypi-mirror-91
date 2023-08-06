# example_publisher.py
import pika, os, logging

from wsit.main.com.vsi.wsi.wsi_buffer import WsiBuffer
from wsit.main.com.vsi.wsi.wsi_utils import WsiUtils

logging.basicConfig()

# Parse CLODUAMQP_URL (fallback to localhost)
url = os.environ.get('CLOUDAMQP_URL', "amqp://nkhqefui:FId5WSVBTAQuuCSZ0RvSpxZ2UBbcEiu9@bear.rmq.cloudamqp.com/nkhqefui")
params = pika.URLParameters(url)
params.socket_timeout = 5

connection = pika.BlockingConnection(params) # Connect to CloudAMQP
channel = connection.channel() # start a channel

# channel.queue_declare('math') # Declare a queue
# channel.exchange_declare(exchange= 'amq.direct', exchange_type='direct')
# channel.queue_bind(exchange='amq.direct', queue='math')
# send a message
number1 = 1
number2 = 2
# wsi_buffer = WsiBuffer.init_by_buffer([1,2,3,4,5,6])
wsi_buffer = WsiBuffer.init_by_buf_size(512)
wsi_buffer.reset_position()
wsi_buffer.put_param_header(2)
wsi_buffer.put_param_entry(8, 1, 4, 0)
wsi_buffer.put_int_d_type(number1, 8)
wsi_buffer.put_param_entry(8, 1, 4, 0)
wsi_buffer.put_int_d_type(number2, 8)

# channel.basic_publish(exchange='amq.direct', routing_key='sum', body=WsiUtils.bytes_to_string(wsi_buffer.get_buffer()))
channel.basic_publish(exchange='amq.direct', routing_key='sum', body="test")
print ("[x] Message sent to consumer")
print(wsi_buffer.get_buffer())
connection.close()
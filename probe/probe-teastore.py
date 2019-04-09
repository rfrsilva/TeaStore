import ast
import sys
import json
import time
from datetime import datetime
import requests
from tmalibrary.probes import *
import subprocess

def create_message():
	# the timestamp is the same for all metrics from this stat variable (Python is not compatible with nanoseconds,
	#  so [:-4] -> microseconds)

	# message to sent to the server API
	# follow the json schema
	# sentTime = current time? Or the same timestamp from the metrics?
	# need to change the probeId, resourceId and messageId

	message = Message(probeId=1, resourceId=101098, messageId=0, sentTime=int(time.time()), data=None)
	line = subprocess.check_output(['tail', '-1', "mylogfile.log"])
	result = [x.strip() for x in line.split(',')]
	temp = result[0]
	count = 0
	responsetime = 0

	while temp == result[0]:
		responsetime = responsetime + int(result[1])
		count = count + 1
		line = subprocess.check_output(['tail', '-1', "mylogfile.log"])
		result = [x.strip() for x in line.split(',')]

	avgrt = responsetime/count
	temp = result[0]


    # Response Time
	# append measurement data to message
	dt = Data(type="measurement", descriptionId=1, observations=None)

    
	obs = Observation(time=int(time.time()), value=avgrt)
	dt.add_observation(observation=obs)

	# append data to message
	message.add_data(data=dt)

	# Throughput
	# append event data to message
	dt = Data(type="measurement", descriptionId=2, observations=None)
	obs = Observation(time=int(time.time()), value=count)
	dt.add_observation(observation=obs)

	# append data to message
	message.add_data(data=dt)
	# return message formatted in json
	return json.dumps(message.reprJSON(), cls=ComplexEncoder)

if __name__ == '__main__':
    # server url as parameter
    url = str(sys.argv[1] + '')
    communication = Communication(url)
    while 1:
     message_formated = create_message()
     response=communication.send_message(message_formated)
     print (response.text)

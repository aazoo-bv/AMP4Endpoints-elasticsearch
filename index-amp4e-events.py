#!/usr/bin/python

import json
import requests
import datetime
from pprint import pprint
from requests.auth import HTTPBasicAuth
from elasticsearch import Elasticsearch

# Set to cron interval
crontime=5
# AMP4Endpoints API ID
amp4e_user=''
# AMP4Endpoints API Password
amp4e_pass=''
# AMP4Endpoints URL
amp4e_url='https://api.eu.amp.cisco.com/v1/events?start_date='

# Elasticsearch index prefix
index_prefix='amp4e-'
# Elasticsearch host, change if not localhost
es = Elasticsearch('127.0.0.1')

# Create timestamp to read data from AMP4Endpoints Event database
timestamp =  datetime.datetime.now() - datetime.timedelta(minutes=crontime)
formatted_timestamp = datetime.datetime.strftime(timestamp, '%Y-%m-%dT%H:%M:%S')

# Format API URL with the timestamp
formatted_url = amp4e_url+formatted_timestamp

# Create index names per day
index_timestamp = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d')
indexname = index_prefix + '-' + index_timestamp

# Get the events
amp4e_events = requests.get(formatted_url, auth=HTTPBasicAuth(amp4e_user,amp4e_pass))
# Parse the events
parsed_json = json.loads(amp4e_events.text)

# Loop through events and index every event
for event in parsed_json['data']:
         es.index(index=indexname, doc_type='amp4e', id=event['id'], body=event)


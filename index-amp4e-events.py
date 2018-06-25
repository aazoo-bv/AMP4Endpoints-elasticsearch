#!/usr/bin/python

import sys
import json
import requests
import datetime
import argparse
#from pprint import pprint
from requests.auth import HTTPBasicAuth
from elasticsearch import Elasticsearch

# Argument sane default options
crontime=5
amp4e_user=''
amp4e_pass=''
amp4e_url='https://api.eu.amp.cisco.com/v1/events?start_date='
index_prefix='amp4e-'
es_host='127.0.0.1'

# Argument parser
parser = argparse.ArgumentParser()

parser.add_argument('--crontime', nargs='?', const=crontime, type=int, help='Set to your cron interval')

parser.add_argument('--amp4e-user', nargs='?', const=amp4e_user, type=str, help='AMP4Endpoints API ID')
parser.add_argument('--amp4e-pass', nargs='?', const=amp4e_pass, type=str, help='AMP4Endpoints API Password')
parser.add_argument('--amp4e-url', nargs='?', const=amp4e_url, type=str, help='AMP4Endpoints URL (including ?start_date=)')

parser.add_argument('--index-prefix', nargs='?', const=index_prefix, type=str, help='Elasticseach index prefix')
parser.add_argument('--es-host', nargs='?', const=es_host, type=str, help='Elasticseach host')

args = parser.parse_args()

# Set arguments
if args.crontime:
	crontime=args.crontime
if args.amp4e_user:
	amp4e_user=args.amp4e_user
if args.amp4e_pass:
	amp4e_pass=args.amp4e_pass
if args.amp4e_url:
	amp4e_url=args.amp4e_url
if args.index_prefix:
	index_prefix=args.index_prefix
if args.es_host:
	es_host=args.es_host

# Actual code running below
es = Elasticsearch(es_host)

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


# *********************************************************************************************
# Program to update dynamodb with latest data from mta feed. It also cleans up stale entried from db
# Usage python dynamodata.py
# *********************************************************************************************
import json,time,sys
from collections import OrderedDict
from threading import Thread
from datetime import datetime
from pytz import timezone
import decimal

import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import tripupdate,vehicle,alert,mtaUpdates,aws

### YOUR CODE HERE ####

# Instantiate mtaUpdates Class with apikey	
mta_updates = mtaUpdates.mtaUpdates('ae83cfea3a7fd03c01ad3e0ea835240e')

# establish dynamoDB client
dynamodb = aws.getResource('dynamodb','us-east-1')
print 'Created dynamoDB Client'

# use existing
table = dynamodb.Table('mtaData')
print 'Accessing "mtaData" Table'

def add_mtadata():
    while(True):
        print 'adding mtadata'
        trips, timestamp = mta_updates.getTripUpdates()
        for tripIDs in trips:
            if trips[tripIDs].vehicleData != None:
                table.put_item(
                        Item={
                          'tripId' : trips[tripIDs].tripId,
                          'routeId' : trips[tripIDs].routeId,                    
                          'startDate' : trips[tripIDs].startDate,
                          'direction' : trips[tripIDs].direction,
                          'currentStopId' : trips[tripIDs].vehicleData.currentStopId,
                          'currentStopStatus' : trips[tripIDs].vehicleData.currentStopStatus,
                          'currentStopNumber' : trips[tripIDs].vehicleData.currentStopNumber,                        
                          'vehicleTimeStamp' : trips[tripIDs].vehicleData.timestamp,                         
                          'futureStopData': trips[tripIDs].futureStops,
                          'timeStamp': timestamp,
                          'localtimeStamp': str(datetime.fromtimestamp(timestamp,timezone('America/New_York')))
                          }
                    )
        print 'Updated table with mtafeed'
        time.sleep(30)
    
def purge_data():
    while(True):
        print 'purging data'
        current_time = time.time()
        purge_time = current_time - 120 # timestamps are in seconds since epoch time

        # first we must scan the table 
        response = table.scan()
        keyList = []
        for i in response['Items']:
            if i['timeStamp'] <= purge_time:
                keyList.append(i['tripId'])
        
        # we scanned and stored the keys to iteratively delete from table
        # this is because there is no batch delete
        for i in keyList:
            table.delete_item(
                Key={'tripId': str(i)}
                )
        
        time.sleep(60)

thread_1 = Thread(name='adding mtadata', target=add_mtadata)
thread_2 = Thread(name='purging data', target=purge_data)

thread_1.start()
thread_2.start()

            
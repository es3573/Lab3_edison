import urllib2,contextlib
from datetime import datetime
from collections import OrderedDict

from pytz import timezone
import gtfs_realtime_pb2
import google.protobuf

import vehicle,alert,tripupdate
import re

class mtaUpdates(object):
    # Do not change Timezone
    TIMEZONE = timezone('America/New_York')
    
    # feed url depends on the routes to which you want updates
    # here we are using feed 1 , which has lines 1,2,3,4,5,6,S
    # While initializing we can read the API Key and add it to the url
    feedurl = 'http://datamine.mta.info/mta_esi.php?feed_id=1&key='
    
    VCS = {1:"INCOMING_AT", 2:"STOPPED_AT", 3:"IN_TRANSIT_TO"}
    tripUpdates = OrderedDict()
    alerts = []
    
    def __init__(self,apikey):
        self.feedurl = self.feedurl + apikey

    # Method to get trip updates from mta real time feed
    def getTripUpdates(self):
        feed = gtfs_realtime_pb2.FeedMessage()
        try:
            with contextlib.closing(urllib2.urlopen(self.feedurl)) as response:
                d = feed.ParseFromString(response.read())
                
        except (urllib2.URLError, google.protobuf.message.DecodeError) as e:
            print "Error while connecting to mta server " +str(e)
        
        timestamp = feed.header.timestamp
        #nytime = datetime.fromtimestamp(timestamp,self.TIMEZONE)
        
        for entity in feed.entity:
            #Trip update represents a change in timetable
            if entity.trip_update and entity.trip_update.trip.trip_id:
                trip_id = entity.trip_update.trip.trip_id
                update = tripupdate.tripupdate()

                update.tripId = entity.trip_update.trip.trip_id
                update.routeId = entity.trip_update.trip.route_id
                update.startDate = entity.trip_update.trip.start_date
                
                # parse trip id for direction
                if (re.search('N', str(entity.trip_update.trip.trip_id))):
                    update.direction = 'N'
                else:
                    update.direction = 'S'
                    
                ### stop_time_update is a LIST ###
                for stop_time_updates in entity.trip_update.stop_time_update:
                    departureTime = None
                    arrivalTime = stop_time_updates.arrival.time
                    stopId = stop_time_updates.stop_id
                    if stop_time_updates.departure:
                        departureTime = stop_time_updates.departure.time
                    update.futureStops[stopId] = [{"arrivalTime": arrivalTime, "departureTime": departureTime}]
                
                self.tripUpdates[trip_id] = update
                
            if entity.vehicle and entity.vehicle.trip.trip_id:
                v = vehicle.vehicle()

                v.currentStopId = entity.vehicle.stop_id
                v.currentStopNumber = entity.vehicle.current_stop_sequence
                v.timestamp = entity.vehicle.timestamp
                v.currentStopStatus = entity.vehicle.current_status
                
                update.vehicleData = v
                
                self.tripUpdates[str(entity.vehicle.trip.trip_id)] = update
                
            
        return self.tripUpdates, timestamp

    # END OF getTripUpdates method

#**********************************************************************************************
# * Copyright (C) 2015-2016 Sareena Abdul Razak sta2378@columbia.edu
# * 
# * This file is part of New-York-MTA-Subway-Trip-Planner.
# * 
# * New-York-MTA-Subway-Trip-Planner can not be copied and/or distributed without the express
# * permission of Sareena Abdul Razak
# * Edited by Peter Wei pw2428@columbia.edu, February 19, 2018
# *********************************************************************************************
# Usage python mta.py

import json,time,csv,sys
from threading import Thread

import boto3
from boto3.dynamodb.conditions import Key,Attr

sys.path.append('../utils')
import aws


DYNAMODB_TABLE_NAME = "mtaData"

# prompt
def prompt():
    print ""
    print ">Available Commands are : "
    print "1. plan trip"
    print "2. subscribe to message feed"
    print "3. exit"  

def buildStationssDB():
    stations = []
    with open('stops.csv', 'rb') as f:
        reader = csv.reader(f)
        for row in reader:
            stations.append(row[0])
    return stations


##############################################
# YOU MAY USE THESE METHODS, OR CODE YOUR OWN
##############################################
# Method to get all local going in a given direction on a give routeId and havent passed sourceStopId
def getLocalTrains(table,direction,routeId,sourceStopId):
    ###############################
    # YOUR CODE HERE #
    ###############################
    return
# Method to get all express going in a given direction on a give routeId and are at given list of stops
def getExpress(table,direction,routeId,stops):
    ###############################
    # YOUR CODE HERE #
    ###############################
    return

# Method to get the earliest train's data
def getEarliestTrain(response,destination):
    ###############################
    # YOUR CODE HERE #
    ############################### 
    return 

def getTimeToReachDestination(trainData,destination):
    ###############################
    # YOUR CODE HERE #
    ###############################
    return





def main():
    dynamodb = aws.getResource('dynamodb','us-east-1')
    snsClient = aws.getClient('sns','us-east-1')
    snsResource = aws.getResource('sns','us-east-1')
    
    dynamoTable = dynamodb.Table(DYNAMODB_TABLE_NAME)

    # Get list of all stopIds
    stations = buildStationssDB()


    while True:
        prompt()
        sys.stdout.write(">select a command : ")
        userIn = sys.stdin.readline().strip()
        if len(userIn) < 1 :
            print "Command not recognized"
        else:
            if userIn == '1':
                sys.stdout.write(">Enter source : ")
                sourceStop = sys.stdin.readline().strip()
                if sourceStop not in stations:
                    sys.stdout.write(">Invalid stop id. Enter a valid stop id")
                    sys.stdout.flush()
                    continue

                sys.stdout.write(">Enter destination : ")
                destinationStop = sys.stdin.readline().strip()
                if destinationStop not in stations:
                    sys.stdout.write(">Invalid stop id. Enter a valid stop id")
                    sys.stdout.flush()
                    continue

                sys.stdout.write(">Type N for uptown, S for downtown: ")
                direction = sys.stdin.readline().strip()

                # Validate direction
                if direction not in ['N','S']:
                    sys.stdout.write(">Invalid direction. Enter a valid direction")
                    sys.stdout.flush()
                    continue
                ###############################
                # YOUR CODE HERE #
                ###############################

            elif userIn == '2':
                sys.stdout.write(">Enter phonenumber")
                phoneNumber = sys.stdin.readline().strip()
                ###############################
                # YOUR CODE HERE #
                ###############################

            else:
                sys.exit()

    

        # check how if there are any 2 or
if __name__ == "__main__":
    main()
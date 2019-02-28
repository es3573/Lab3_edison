# Group SGWW
# Erik Su (es3573)
# Pengchong Wang (pw2480)
# Xin Geng (xg2294)

import mraa
import time
import math

import boto3

def convert_temp(raw_data):
    R0 = 100000
    B = 4275
    
    R = 1023.0/(raw_data)-1.0;
    R = R0*R;
    temperature = 1.0/(math.log(R/R0)/B+1/298.15)-273.15
    return temperature

# Initialize client
snsClient = aws.getClient('sns','us-east-1')
topic_arn = 'arn:aws:sns:us-east-1:096527816675:temperature'

# Initialize temp sensor and get reading 
tempSensor = mraa.Aio(1)
current_temp = convert_temp(tempSensor.read())

msg = "The current temperature surrounding Intel Edison: " + str(current_temp)
subj = "SNS message over boto3"
response = snsClient.publish(
                TopicArn=topic_arn,
                Subject = subj,
                Message = msg
                )










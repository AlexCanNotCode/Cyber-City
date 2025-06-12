import boto3
import json

#initialize dynamo DB client:

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('CyberCrowds')

# Load Data

rides = [
    {'GuestID': 'ride-1', 'name': 'The Hyper Drive', 'waitTime': 15},
    {'GuestID': 'ride-2', 'name': 'Traina Train', 'waitTime': 35},
    {'GuestID': 'ride-3', 'name': 'Cyber Coaster', 'waitTime': 45},
    {'GuestID': 'ride-4', 'name': 'Speed Street', 'waitTime': 68},
    {'GuestID': 'ride-5', 'name': 'Cyber Drop', 'waitTime': 27}
]

for ride in rides:
    response = table.put_item(Item=ride)

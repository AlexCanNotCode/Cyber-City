import json
import boto3
from datetime import datetime
import os

def lambda_handler(event, context):
    """
    AWS Lambda function to fetch ride wait times from DynamoDB
    and return them in the format expected by the display interface
    """
    
    # Initialize DynamoDB client
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    
    table_name = 'CyberCrowds'
    
    try:
        # Scan the table for all ride data
        response = dynamodb.scan(
            TableName=table_name,
            FilterExpression='begins_with(GuestID, :ride_prefix)',
            ExpressionAttributeValues={
                ':ride_prefix': {'S': 'ride-'}
            }
        )
        
        rides = []
        for item in response['Items']:
            # Convert DynamoDB item to the expected format
            ride = {
                'id': int(item.get('id', {}).get('N', '0')),
                'name': item.get('name', {}).get('S', ''),
                'status': item.get('status', {}).get('S', 'open'),
                'category': item.get('category', {}).get('S', ''),
                'type': item.get('type', {}).get('S', ''),
                'imageUrl': item.get('imageUrl', {}).get('S'),
                'capacity': item.get('capacity', {}).get('S'),
                'lastUpdated': item.get('lastUpdated', {}).get('S', datetime.now().isoformat())
            }
            
            # Handle waitTime (only for rides, not shows)
            if 'waitTime' in item:
                ride['waitTime'] = int(item['waitTime']['N']) if item['waitTime']['N'] != '0' or ride['status'] != 'maintenance' else None
            else:
                ride['waitTime'] = None
            
            # Handle nextShowTime (for shows)
            if 'nextShowTime' in item:
                ride['nextShowTime'] = item['nextShowTime']['S']
            else:
                ride['nextShowTime'] = None
                
            rides.append(ride)
        
        # Sort rides by ID for consistent ordering
        rides.sort(key=lambda x: x['id'])
        
        if not rides:
            return {
                'statusCode': 400,
                'body': json.dumps("No ride wait times found.")
            }
        
        # Return the formatted response
        response_data = {
            'rides': rides,
            'lastUpdated': datetime.now().isoformat()
        }
        
        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps(response_data)
        }
        
    except Exception as e:
        print(f"Error fetching ride data: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*'
            },
            'body': json.dumps({
                'error': 'Internal server error',
                'message': str(e)
            })
        }

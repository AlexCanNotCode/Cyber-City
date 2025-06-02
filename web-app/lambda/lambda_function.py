import json
import boto3
from datetime import datetime

def lambda_handler(event, context):
    dynamodb = boto3.client('dynamodb', region_name='us-east-1')
    table_name = 'CyberCrowds'

    try:
        # Scan for all rides starting with "ride-"
        response = dynamodb.scan(
            TableName=table_name,
            FilterExpression='begins_with(GuestID, :prefix)',
            ExpressionAttributeValues={
                ':prefix': {'S': 'ride-'}
            }
        )

        items = response.get('Items', [])
        if not items:
            return {
                'statusCode': 404,
                'headers': {
                    'Content-Type': 'application/json',
                    'Access-Control-Allow-Origin': '*'
                },
                'body': json.dumps({'error': 'No rides found'})
            }

        # Build a list of rides
        rides = []
        for item in items:
            name = item.get('name', {}).get('S', 'Unknown')
            wait = item.get('waitTime', {}).get('N', '0')
            rides.append({
                'ride': name,
                'wait_time': f"{wait} mins"
            })

        return {
            'statusCode': 200,
            'headers': {
                'Content-Type': 'application/json',
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'GET, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type'
            },
            'body': json.dumps({'rides': rides})
        }

    except Exception as e:
        print(f"Error: {str(e)}")
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

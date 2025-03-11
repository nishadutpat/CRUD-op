import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table_name = os.environ['DYNAMODB_TABLE']
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    http_method = event.get('httpMethod', '')

    if http_method == 'POST':
        return add_user(event)
    elif http_method == 'GET':
        return get_users()
    elif http_method == 'DELETE':
        return delete_user(event)
    else:
        return {
            'statusCode': 400,
            'body': json.dumps({'message': 'Unsupported method'})
        }

def add_user(event):
    try:
        body = json.loads(event['body'])
        table.put_item(Item=body)
        return {
            'statusCode': 201,
            'body': json.dumps({'message': 'User added successfully'})
        }
    except Exception as e:
        return error_response(str(e))

def get_users():
    try:
        response = table.scan()
        return {
            'statusCode': 200,
            'body': json.dumps(response.get('Items', []))
        }
    except Exception as e:
        return error_response(str(e))

def delete_user(event):
    try:
        user_id = event['queryStringParameters']['UserID']
        table.delete_item(Key={'UserID': user_id})
        return {
            'statusCode': 200,
            'body': json.dumps({'message': 'User deleted successfully'})
        }
    except Exception as e:
        return error_response(str(e))

def error_response(error_message):
    return {
        'statusCode': 500,
        'body': json.dumps({'error': error_message})
    }

import json
import boto3
import uuid

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table("deplo_table")

def lambda_handler(event, context):
    path = event.get("resource")
    http_method = event.get("httpMethod")

    origin = event.get("headers", {}).get("origin", "*")

    
    if http_method == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": {
                "Access-Control-Allow-Origin": origin,
                "Access-Control-Allow-Methods": "POST, GET, DELETE, OPTIONS",
                "Access-Control-Allow-Headers": "Content-Type"
            },
            "body": json.dumps({"message": "CORS preflight success"})
        }

    if path == "/user":
        if http_method == "POST":
            return create_user(event, origin)
        elif http_method == "GET":
            return get_users(origin)
        elif http_method == "DELETE":
            return delete_user(event, origin)
        else:
            return {
                "statusCode": 400,
                "headers": {"Access-Control-Allow-Origin": origin},
                "body": json.dumps({"error": f"Unsupported HTTP method: {http_method}"})
            }
    else:
        return {
            "statusCode": 404,
            "headers": {"Access-Control-Allow-Origin": origin},
            "body": json.dumps({"error": "Invalid resource path"})
        }

def create_user(event, origin):
    body = json.loads(event["body"])
    user_id = str(uuid.uuid4())
    user_data = {
        "id": user_id,
        "Name": body["Name"],
        "Email": body["Email"]
    }
    table.put_item(Item=user_data)
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": origin},
        "body": json.dumps({"message": "User added successfully", "id": user_id})
    }

def get_users(origin):
    response = table.scan()
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": origin},
        "body": json.dumps(response["Items"])
    }

def delete_user(event, origin):
    body = json.loads(event["body"])
    user_id = body["id"]
    table.delete_item(Key={"id": user_id})
    return {
        "statusCode": 200,
        "headers": {"Access-Control-Allow-Origin": origin},
        "body": json.dumps({"message": "User deleted successfully"})
    }

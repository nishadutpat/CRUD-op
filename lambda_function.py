import json
import boto3
import os

# Initialize DynamoDB
dynamodb = boto3.resource("dynamodb")
table_name = os.getenv("DYNAMODB_TABLE", "deplo_table")  # Replace with your table name
table = dynamodb.Table(table_name)

def lambda_handler(event, context):
    http_method = event["httpMethod"]
    path = event["path"]

    if http_method == "POST" and path == "/users":
        return create_user(event)

    elif http_method == "GET" and path == "/users":
        return get_users()

    elif http_method == "DELETE" and path.startswith("/users/"):
        user_id = path.split("/")[-1]
        return delete_user(user_id)

    else:
        return {
            "statusCode": 400,
            "body": json.dumps({"message": "Invalid request"})
        }

def create_user(event):
    try:
        body = json.loads(event["body"])
        user_id = body.get("UserID")
        name = body.get("Name")
        email = body.get("Email")

        if not user_id or not name or not email:
            return {"statusCode": 400, "body": json.dumps({"message": "All fields are required"})}

        table.put_item(Item={"UserID": user_id, "Name": name, "Email": email})

        return {"statusCode": 200, "body": json.dumps({"message": "User added successfully"})}
    
    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def get_users():
    try:
        response = table.scan()
        users = response.get("Items", [])

        return {"statusCode": 200, "body": json.dumps(users)}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

def delete_user(user_id):
    try:
        table.delete_item(Key={"UserID": user_id})
        return {"statusCode": 200, "body": json.dumps({"message": "User deleted successfully"})}

    except Exception as e:
        return {"statusCode": 500, "body": json.dumps({"message": str(e)})}

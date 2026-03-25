import json
import boto3
import uuid
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET,POST,PUT,DELETE"
}

def lambda_handler(event, context):
    if event.get("httpMethod") == "OPTIONS":
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": ""
        }

    body = json.loads(event["body"])

    content = body.get("content")
    custom_id = body.get("id")

    if not content:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"message": "Missing content"})
        }

    if custom_id and str(custom_id).strip():
        note_id = str(custom_id).strip()
    else:
        note_id = str(uuid.uuid4())

    existing_note = table.get_item(Key={"id": note_id}).get("Item")
    if existing_note:
        return {
            "statusCode": 409,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "message": "A note with that ID already exists",
                "id": note_id
            })
        }

    item = {
        "id": note_id,
        "content": content
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "message": "Note created",
            "id": note_id
        })
    }
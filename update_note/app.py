import json
import boto3
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

    note_id = event["pathParameters"]["id"]
    body = json.loads(event["body"])

    content = body.get("content")

    if not content:
        return {
            "statusCode": 400,
            "headers": CORS_HEADERS,
            "body": json.dumps({"message": "Missing content"})
        }

    response = table.update_item(
        Key={"id": note_id},
        UpdateExpression="SET content = :c",
        ExpressionAttributeValues={
            ":c": content
        },
        ReturnValues="ALL_NEW"
    )

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS,
        "body": json.dumps({
            "message": "Note updated",
            "note": response["Attributes"]
        })
    }
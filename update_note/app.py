import json
import boto3
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    note_id = event["pathParameters"]["id"]
    body = json.loads(event["body"])

    content = body.get("content")

    if not content:
        return {
            "statusCode": 400,
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
        "body": json.dumps({
            "message": "Note updated",
            "note": response["Attributes"]
        })
    }
import json
import boto3
import uuid
import os

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["TABLE_NAME"])

def lambda_handler(event, context):
    body = json.loads(event["body"])

    note_id = str(uuid.uuid4())

    item = {
        "id": note_id,
        "content": body["content"]
    }

    table.put_item(Item=item)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "Note created",
            "id": note_id
        })
    }
import boto3
import logging
import datetime
from botocore.exceptions import ClientError
import os
import uuid

bedrock_client = boto3.client(service_name="bedrock-runtime")
ddb_client = boto3.client(service_name="dynamodb")

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

DDB_NAME = os.environ.get("DDB_TABLE_NAME")

def write_to_dynamodb(table_name, user_message, output_message):
    try:
        response = ddb_client.put_item(
            TableName=table_name,
            Item={
                'id': {'S': str(uuid.uuid4())},
                'userMessage': {'S': user_message},
                'outputMessage': {'S': str(output_message)},
                'timestamp': {'S': datetime.datetime.now().isoformat()}
            }
        )
        logger.info("Successfully wrote to DynamoDB")
        return response
    except ClientError as e:
        logger.error(f"Error writing to DynamoDB: {e.response['Error']['Message']}")
        raise

def generate_conversation(bedrock_client, model_id, system_prompt, messages):
  temperature = 0.5
  top_k = 200

  inference_config = {"temperature": temperature}
  additional_model_fields = {"top_k": top_k}

  response = bedrock_client.converse(
    modelId=model_id,
    messages=messages,
    system=system_prompt,
    inferenceConfig=inference_config,
    additionalModelRequestFields=additional_model_fields,
  )

  return response

def handler(event, context):
  messages = []

  model_id = "anthropic.claude-3-sonnet-20240229-v1:0"
  system_prompt = [{"text": "You are an app that creates playlists for a radio station that plays rock and pop music."
                       "Only return song names and the artist."}]

  message = {
    "role": "user",
    "content": [{"text": event["message"]}]
  }

  try:
    messages.append(message)
    response = generate_conversation(bedrock_client=bedrock_client, model_id=model_id, system_prompt=system_prompt, messages=messages)
    output_message = response["output"]["message"]
    print(output_message)
    write_to_dynamodb(table_name=DDB_NAME, user_message=event["message"], output_message=output_message)
    return {
      "statusCode": 200,
      "body": output_message["content"][0]["text"]
    }
  except ClientError as err:
    message = err.response["Error"]["Message"]
    logger.error("A client error ocurred: %s", message)
    print(f"A client error ocurred: {message}")
  else:
    print("Done")


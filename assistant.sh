#!/bin/bash

# Check if a message was provided
if [ $# -eq 0 ]; then
    echo "Please provide a message."
    echo "Usage: sh lambdabedrock.sh \"your message here\""
    exit 1
fi

# The message passed as an argument
MESSAGE="$1"

# Your Lambda function name
FUNCTION_NAME="CdkIntroStack-LambdaBedrock8CBD5FA3-FEe2s0IBSnvV"

# Invoke the Lambda function
aws lambda invoke \
    --function-name $FUNCTION_NAME \
    --payload "{\"message\": \"$MESSAGE\"}" \
    --cli-binary-format raw-in-base64-out \
    output.txt

# Check if the invocation was successful
if [ $? -eq 0 ]; then
    echo "Lambda function invoked successfully."
    echo "Response:"
    cat output.txt
else
    echo "Failed to invoke Lambda function."
fi

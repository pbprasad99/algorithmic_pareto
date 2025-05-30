#!/bin/sh -v

# -----------------------------------------------------------------
# Configure the AWS CLI to let it communicate with your account
# -----------------------------------------------------------------
aws configure set aws_access_key_id $aws_access_key_id
aws configure set aws_secret_access_key $aws_secret_access_key
aws configure set region us-east-1

# -----------------------------------------------------------------
# Create and deploy a stack
# -----------------------------------------------------------------
aws cloudformation deploy \
    --template-file Stack.json \
    --stack-name CloudResources \
    --capabilities CAPABILITY_NAMED_IAM \
    --region us-east-1

policy_arn=`aws cloudformation describe-stacks --stack-name CloudResources | jq -r '.Stacks[0].Outputs[] | select(.OutputKey=="CustomPolicyARN") | .OutputValue'`

echo $policy_arn
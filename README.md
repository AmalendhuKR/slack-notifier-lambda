# Slack Notifier via AWS Lambda

## Overview

This AWS Lambda function sends Slack notifications via an Incoming Webhook URL, triggered through API Gateway and deployed using CloudFormation.

## Get a Slack Webhook URL

    1. Go to Slack Webhooks.
    2. Create a Slack App → From scratch → Name it → Select Workspace
    3. Enable Incoming Webhooks
    4. Add New Webhook to Workspace → Select channel → Copy Webhook URL

## Deployment

### Prepare the Package

```
mkdir package
pip install -r requirements.txt -t package/
cp app.py package/
cd package
zip -r ../lambda.zip .
//in windows
Compress-Archive -Path package\* -DestinationPath lambda_function.zip
cd ..
```

### Upload the Lambda Code to S3

```
aws s3 cp slack_notifier.zip s3://your-s3-bucket/
```

### Deploy CloudFormation Stack

```
aws cloudformation create-stack --stack-name SlackNotifier \
  --template-body file://cloudformation-template.yml \
  --parameters ParameterKey=S3Bucket,ParameterValue=your-s3-bucket \
               ParameterKey=S3Key,ParameterValue=lambda.zip \
               ParameterKey=SlackWebhookUrl,ParameterValue=your-webhook-url \
  --capabilities CAPABILITY_NAMED_IAM \
  --role-arn arn:aws:iam::your-account-id:role/your-cloudformation-execution-role

```

### Cleanup

```
aws cloudformation delete-stack --stack-name SlackNotifierStack
```

### Local Testing

```
py ./test/local.py
```

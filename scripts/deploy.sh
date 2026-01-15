#!/bin/bash

set -e

echo "🚀 AWS Weather Alert System - Deployment Script"
echo "================================================"

if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    echo "   Please copy config/.env.example to .env and configure it"
    exit 1
fi

source .env

STACK_NAME=${STACK_NAME:-weather-alert-system}
REGION=${AWS_REGION:-us-east-1}

echo ""
echo "📝 Configuration:"
echo "   Stack Name: $STACK_NAME"
echo "   Region: $REGION"
echo "   City: $CITY_NAME"
echo "   Alert Email: $ALERT_EMAIL"
echo ""

read -p "Continue with deployment? (y/n) " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Deployment cancelled"
    exit 0
fi

echo ""
echo "📦 Step 1: Installing dependencies..."
cd src
pip install -r ../requirements.txt -t . --quiet
cd ..

echo "✅ Dependencies installed"
echo ""
echo "🏗️  Step 2: Deploying CloudFormation stack..."

aws cloudformation deploy \
    --template-file infrastructure/template.yaml \
    --stack-name $STACK_NAME \
    --parameter-overrides \
        CityName=$CITY_NAME \
        Latitude=$LAT \
        Longitude=$LON \
        AlertEmail=$ALERT_EMAIL \
        ScheduleExpression="$SCHEDULE_EXPRESSION" \
    --capabilities CAPABILITY_IAM \
    --region $REGION

if [ $? -eq 0 ]; then
    echo "✅ Stack deployed successfully"
else
    echo "❌ Stack deployment failed"
    exit 1
fi

echo ""
echo "📊 Step 3: Getting stack outputs..."

BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' \
    --output text)

LAMBDA_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`LambdaFunctionName`].OutputValue' \
    --output text)

SNS_TOPIC=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`SNSTopicArn`].OutputValue' \
    --output text)

echo ""
echo "✅ Deployment Complete!"
echo "================================================"
echo ""
echo "📦 Resources Created:"
echo "   S3 Bucket: $BUCKET_NAME"
echo "   Lambda Function: $LAMBDA_NAME"
echo "   SNS Topic: $SNS_TOPIC"
echo ""
echo "⚠️  IMPORTANT: Check your email and confirm the SNS subscription!"
echo ""
echo "🧪 Test the function:"
echo "   aws lambda invoke --function-name $LAMBDA_NAME response.json"
echo ""
echo "📊 View logs:"
echo "   aws logs tail /aws/lambda/$LAMBDA_NAME --follow"
echo ""

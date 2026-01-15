#!/bin/bash

set -e

echo "🗑️  AWS Weather Alert System - Cleanup Script"
echo "=============================================="

if [ ! -f .env ]; then
    echo "❌ Error: .env file not found"
    exit 1
fi

source .env

STACK_NAME=${STACK_NAME:-weather-alert-system}
REGION=${AWS_REGION:-us-east-1}

echo ""
echo "⚠️  WARNING: This will delete all resources!"
echo "   Stack: $STACK_NAME"
echo "   Region: $REGION"
echo ""

read -p "Are you sure you want to continue? (yes/no) " -r
echo

if [[ ! $REPLY == "yes" ]]; then
    echo "Cleanup cancelled"
    exit 0
fi

echo ""
echo "🔍 Getting bucket name..."

BUCKET_NAME=$(aws cloudformation describe-stacks \
    --stack-name $STACK_NAME \
    --region $REGION \
    --query 'Stacks[0].Outputs[?OutputKey==`BucketName`].OutputValue' \
    --output text 2>/dev/null || echo "")

if [ ! -z "$BUCKET_NAME" ]; then
    echo "🗑️  Emptying S3 bucket: $BUCKET_NAME"
    aws s3 rm s3://$BUCKET_NAME --recursive --region $REGION
    echo "✅ Bucket emptied"
else
    echo "⚠️  No bucket found (may have been deleted already)"
fi

echo ""
echo "🗑️  Deleting CloudFormation stack..."

aws cloudformation delete-stack \
    --stack-name $STACK_NAME \
    --region $REGION

echo "⏳ Waiting for stack deletion..."

aws cloudformation wait stack-delete-complete \
    --stack-name $STACK_NAME \
    --region $REGION

echo ""
echo "✅ Cleanup Complete!"
echo "   All resources have been deleted"
echo ""
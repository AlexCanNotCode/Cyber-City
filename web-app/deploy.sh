#!/bin/bash

set -e

# VARIABLES
AWS_REGION="us-east-1"
REPO_NAME="waittime-web"
IMAGE_TAG="latest"

echo "🧱 Building Docker image..."
docker build -t $REPO_NAME .

echo "🔐 Logging into ECR..."
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin \
  $(aws sts get-caller-identity --query 'Account' --output text).dkr.ecr.$AWS_REGION.amazonaws.com

ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
ECR_URL="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME"

echo "🛠️ Running Terraform deployment..."
cd terraform
terraform init
terraform apply -auto-approve

echo "📤 Tagging and pushing Docker image to ECR..."
docker tag $REPO_NAME:latest $ECR_URL:$IMAGE_TAG
docker push $ECR_URL:$IMAGE_TAG

echo "🌐 Injecting API Gateway URL into script.js..."
API_URL=$(terraform output -raw api_url)
cd ../web
sed -i "s|https://PLACEHOLDER_API_URL|$API_URL|g" script.js

echo "✅ Deployment complete. App should be live via ECS!"

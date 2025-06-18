#!/bin/bash

AWS_REGION="us-east-1"
REPO_NAME="waittime-web"
IMAGE_TAG="latest"

echo "Rebuilding and pushing Docker image..."
docker build -t $REPO_NAME .
ACCOUNT_ID=$(aws sts get-caller-identity --query 'Account' --output text)
ECR_URL="$ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$REPO_NAME"
docker tag $REPO_NAME:$IMAGE_TAG $ECR_URL:$IMAGE_TAG
docker push $ECR_URL:$IMAGE_TAG

echo "Forcing ECS redeploy..."
aws ecs update-service \
  --cluster waittime-cluster \
  --service waittime-web-service \
  --region $AWS_REGION \
  --force-new-deployment

echo "Done! New code is live."

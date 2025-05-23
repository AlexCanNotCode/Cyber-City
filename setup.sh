#!/bin/bash

# Install Terraform on Amazon Linux
sudo yum install -y yum-utils
sudo yum-config-manager --add-repo https://rpm.releases.hashicorp.com/AmazonLinux/hashicorp.repo
sudo yum -y install terraform

cd web-app/terraform
terraform init                # Initialize Terraform
terraform plan                # Optional: preview what will be created
terraform apply    

API_URL=$(terraform output -raw api_url)
sed -i "s|https://PLACEHOLDER_API_URL|$API_URL|g" ../web/script.js

docker build -t waittime-web .
docker run -p 80:80 waittime-web

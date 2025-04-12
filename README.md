# Build Docker image for AWS Lambda
docker buildx build --platform linux/amd64 -t task-manager-lambda . --load

# Tag the image
docker tag task-manager-lambda:latest 581408947454.dkr.ecr.us-west-1.amazonaws.com/task-manager-lambda:latest

# Login to ECR
aws ecr get-login-password --region us-west-1 | docker login --username AWS --password-stdin 581408947454.dkr.ecr.us-west-1.amazonaws.com

# Push to ECR
docker push 581408947454.dkr.ecr.us-west-1.amazonaws.com/task-manager-lambda:latest


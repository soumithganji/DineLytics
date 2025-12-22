---
description: Deploy DineLytics to AWS App Runner
---

To deploy the DineLytics application to AWS, we will use **AWS App Runner**, which provides a simple, fully managed service for containerized applications.

### Prerequisites

1.  **AWS Account**: Ensure you have an active account.
2.  **AWS CLI**: Configure with `aws configure`.
3.  **Docker**: Ensure Docker is running.

### Deployment Steps

#### 1. Create ECR Repository

Create a repository to store your Docker image.

```bash
aws ecr create-repository --repository-name dinelytics --region us-east-1
```

#### 2. Authenticate Docker

Login to ECR. Replace `<ACCOUNT_ID>` with your AWS Account ID (found via `aws sts get-caller-identity`).

```bash
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin <ACCOUNT_ID>.dkr.ecr.us-east-1.amazonaws.com
```

#### 3. Build & Push

Build the image for linux/amd64 (required for App Runner if you are on M1/M2 Mac) and push it.

```bash
# Set your account ID variable
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
export REGION=us-east-1
export REPO_URI=$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/dinelytics

# Build
docker build --platform=linux/amd64 -t dinelytics .

# Tag
docker tag dinelytics:latest $REPO_URI:latest

# Push
docker push $REPO_URI:latest
```

#### 4. Create App Runner Service

1.  Open the [App Runner Console](https://console.aws.amazon.com/apprunner).
2.  Click **Create service**.
3.  **Source**: "Container registry" > "Amazon ECR".
4.  **Image**: Select the `dinelytics` image.
5.  **Configuration**:
    *   **Port**: `8501`
    *   **Environment Variables**: Add the following from your `.env`:
        *   `OPENAI_API_KEY`
        *   `MONGO_URI`
        *   `PINECONE_API_KEY`
        *   `ASSISTANT_NAME`
        *   (And any others in your .env)
6.  **Deploy**.

#### 5. Verification

Once the service status is "Running", click the provided default domain URL to access your app.

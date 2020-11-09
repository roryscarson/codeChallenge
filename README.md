Coding Challenge summarized requirements
* Write new file to S3 every 2 minutes.
* Logging to stderr
* 24hr life cycle on files, contain sensitive info, 100% availability
* MMDDYYYY-time-filename
* Docker within k8s, QA and Stage


# Create the initial infrastructure
##### Modify the variables.tf files
replace "rcarson-inra-test" with something else. S3 buckets are unique globally
across all accounts so names cannot be shared.

# Terraform the bucket
##### This will create the S3 buckets used to store the files
```
cd codeChallenge/infrastructure/qa  
terraform init  
terraform apply  
```
```
cd codeChallenge/infrastructure/staging
terraform init
terraform apply
```

# Build and deploy container
##### replace BUCKET_NAME, ACCESS_KEY, and SECRET_ACCESS_KEY with your own values

-> codeChallenge/app
```
docker build -f Dockerfile -t filemaker:latest .
docker run -p 5001:5000 --name="filemaker" -e ENVIRONMENT=staging -e BUCKET_NAME=YOUR_BUCKET_NAME -e ACCESS_KEY=REDACTED -e SECRET_ACCESS_KEY=REDACTED filemaker:latest
```

# Deploy to kubernetes
##### set your environment context
```
kubectl config use-context your-environment-stage
```
##### Create the secrets config for storing access keys. Keys must match from the previous step
```
kubectl create secret generic codechallenge-secrets --from-literal=access_key=REDACTED --from-literal=secret_access_key=REDACTED
```
##### apply deployment file
```
kubectl apply -f stage.yml
```

/*
Requirements:
1) Write new file to S3 every 2 minutes.
2) Logging to stderr
3) 24hr life cycle on files, contain sensitive info, 100% availability
4) MMDDYYYY-time-filename
5) Docker within k8s, QA and Stage

You need to develop and deploy a python app that writes a new file to S3 every 2 minutes.
You don’t need to provide tests but you need to be sure it works whenever we try to deploy it.
All logging should be redirected to stderr.

The files that the app works with need to be maintained only for 24h and
they are super important and need to be protected at all costs
- we cannot afford to lose them and they should be treated
as if they contain sensitive information.

The content of the file is not important (we suggest simply inserting "Programming is fun!"
and the mtime), however file names should be prepended with the creation date and time.

The app (including its' logging) needs to be running as a
Docker container for two environments - QA and staging.
The staging environment should be as similar as possible to live for testing purposes.
We will be using Terraform to deploy your project,
which includes using Kubernetes to provision the docker containers.
Please keep this in mind.
*/

resource "aws_s3_bucket" "input_bucket" {
  bucket = "${var.bucket_name}-${var.environment}"
  acl    = "private"

  lifecycle_rule {
    prefix  = ""
    enabled = true

    # Garbage collect incomplete/aborted multipart uploads
    abort_incomplete_multipart_upload_days = "1"

    expiration {
      # Delete objects older than 1 days.
      days = 1
    }
  }

  tags = {
    Name        = var.bucket_name
    Environment = var.environment
  }
}

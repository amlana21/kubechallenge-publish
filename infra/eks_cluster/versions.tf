terraform {
  required_version = ">= 0.14"

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">= 3.72"
    }
  }

  backend "s3" {
    bucket = "<state_bucket_name>"
    key    = "kubecluster"
    region = "us-east-1"
  }
}

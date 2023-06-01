variable "bucket_name" {
  description = "Value of the Name tag for the S3 Bucket"
  type        = string
  default     = "example_bucket"
}

variable "role" {
  description = "Name of Identity and Access Management (IAM) Role"
  type        = string
  default     = "example_role"
}
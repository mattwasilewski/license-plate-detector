resource "aws_iam_role" "example_role" {
  name               = "example_role"
  assume_role_policy = jsonencode({
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = {
        Service = "lambda.amazonaws.com"
      }
    }]
    Version   = "2012-10-17"
  })
}

resource "aws_s3_bucket" "example_bucket" {
  bucket = "cloudclimbersbucket"
}

resource "aws_lambda_function" "example_lambda" {
  filename      = "lambda_handler.zip"
  function_name = "lambda_handler"
  role          = aws_iam_role.example_role.arn
  handler       = "lambda_handler.lambda_handler"
  runtime       = "python3.8"
  timeout       = 300
  memory_size   = 256
  source_code_hash = filebase64sha256("lambda_handler.zip")
}

resource "aws_s3_bucket_object" "python_code" {
  bucket       = aws_s3_bucket.example_bucket.id
  key          = "lambda_handler.zip"
  source       = "lambda_handler.zip"
}

resource "aws_s3_bucket_object" "requirements" {
  bucket       = aws_s3_bucket.example_bucket.id
  key          = "requirements.txt"
  source       = "requirements.txt"
}
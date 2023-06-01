# License Plate Detection Application

This application is designed to detect Polish license plates from a video file stored in an Amazon S3 bucket and save the results in a JSON file format, also stored in S3. It utilizes various AWS services, including S3, Rekognition, Lambda, IAM, and CloudWatch.

## AWS Services Used

- **Amazon S3**: Used for storing the input video file and the output JSON file.
- **Amazon Rekognition**: Used for license plate detection from the video frames.
- **AWS Lambda**: Executes the license plate detection logic and interacts with S3 and Rekognition.
- **IAM**: Manages the application's permissions and access control.
- **CloudWatch**: Monitors and logs application events and metrics.

## Prerequisites

Before deploying the application, ensure that you have the following:

- An AWS account with appropriate permissions to create and manage the required services.
- Terraform installed on your local machine.

## Deployment Instructions

1. Clone the repository and navigate to the project directory.
2. Open the `variables.tf` file and set the values for the following variables:
   - `role` - IAM role ARN for the Lambda function.
   - `bucket_name` - Name of the S3 bucket where the video and JSON files will be stored.
3. Save the changes to the `variables.tf` file.
4. Open the AWS Lambda function configuration in the AWS Management Console.
5. Add the following environment variables to the Lambda function configuration:
   - `BUCKET_NAME` - Set the value to the S3 bucket name.
   - `FILE_NAME` - Set the value to the name of the video file.
   - `ROLE_ARN` - Set the value to the IAM role ARN.
6. Save the environment variable changes in the Lambda function configuration.
7. Open a terminal or command prompt and navigate to the project directory.
8. Initialize Terraform by running the following command: `terraform init`
9. Deploy the application using Terraform: `terraform apply`
10. Once the deployment is complete, the application will be up and running, ready to process the video file and save the results in S3.

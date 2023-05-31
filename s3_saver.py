import boto3
import json

class S3Saver:
    def save_data_s3(self, bucket, results):
        s3 = boto3.resource('s3')
        json_data = {'license_plates': results}
        s3.Object(bucket, 'output.json').put(Body=json.dumps(json_data))
import boto3
import json
import logging

class S3Saver:
    def save_data_s3(self, bucket, results):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        s3 = boto3.resource('s3')
        json_data = {'license_plates': results}
        s3.Object(bucket, 'output.json').put(Body=json.dumps(json_data))
        logging.info('Data saved in S3')
import boto3

class RekognitionService:
    def __init__(self):
        self.client = boto3.client('rekognition')

    def start_text_detection(self, video):
        response = self.client.start_text_detection(
            Video={'S3Object': {'Bucket': video['bucket'], 'Name': video['file']}}
        )
        return response

    def get_text_detection_results(self, job_id, next_token=''):
        max_results = 100
        response = self.client.get_text_detection(
            JobId=job_id,
            MaxResults=max_results,
            NextToken=next_token
        )
        return response
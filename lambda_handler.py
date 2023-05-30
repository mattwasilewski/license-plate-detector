import boto3
import json
import logging
import re
from datetime import timedelta

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class VideoDetect:
    def __init__(self, role, bucket, video, rek, results):
        self.roleArn = role
        self.bucket = bucket
        self.video = video
        self.rek = rek
        self.results = results

    def StartTextDetection(self):
        response = self.rek.start_text_detection(
            Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}}
        )
        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)

    def validate_license_plate(self, text):
        pattern = r'^[A-Z]{2}\s?\d{2,3}[A-Z0-9]{1,2}$'
        if re.match(pattern, text):
            return True
        else:
            return False

    def save_data_s3(self, detected_texts):
        s3 = boto3.resource('s3')
        json_data = {'license_plates': detected_texts}
        s3.Object(self.bucket, 'output.json').put(Body=json.dumps(json_data))


    def process_license_plate(self, license_plate, timestamp):
        current_time = str(timedelta(milliseconds=timestamp))
        if license_plate in self.results:
            self.results[license_plate].append(current_time)
        else:
            self.results[license_plate] = [current_time]
    

    def GetTextDetectionResults(self):
        maxResults = 100
        paginationToken = ''
        finished = False
        while not finished:
            response = self.rek.get_text_detection(
                JobId=self.startJobId,
                MaxResults=maxResults,
                NextToken=paginationToken
            )

            if response['JobStatus'] == "IN_PROGRESS":
                continue
            else:
                for detection in response['TextDetections']:
                    detected_text = detection['TextDetection']['DetectedText']
                    timestamp = detection['Timestamp']
                    if self.validate_license_plate(detected_text):
                        self.process_license_plate(detected_text, timestamp)
                        print(detected_text)
                        print(timestamp)

                self.save_data_s3(self.results)
                finished = True



def lambda_handler(event, context):
    roleArn = event['role']
    bucket = event['bucket']
    video = event['file']
    results = {}

    session = boto3.Session()
    rek = session.client('rekognition')

    analyzer = VideoDetect(roleArn, bucket, video, rek, results)
    analyzer.StartTextDetection()
    analyzer.GetTextDetectionResults()

    return {
        'statusCode': 200,
        'body': json.dumps('Video analysis completed!')
    }
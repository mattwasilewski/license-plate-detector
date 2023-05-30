import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

class VideoDetect:
    def __init__(self, role, bucket, video, rek):
        self.roleArn = role
        self.bucket = bucket
        self.video = video
        self.rek = rek

    def StartTextDetection(self):
        response = self.rek.start_text_detection(
            Video={'S3Object': {'Bucket': self.bucket, 'Name': self.video}}
        )
        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)

    def GetTextDetectionResults(self):
        maxResults = 20
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
                detected_texts = []
                for detection in response['TextDetections']:
                    detected_text = detection['TextDetection']['DetectedText']
                    if detected_text not in ["Camera", "Regular Camera", "LPR Camera"]:
                        detected_texts.append(detected_text)
                        print(detected_text)     
                finished = True

def lambda_handler(event, context):
    role = event['role']
    bucket = event['bucket']
    video = 'test.mp4'

    session = boto3.Session()
    rek = session.client('rekognition')

    analyzer = VideoDetect(role, bucket, video, rek)
    analyzer.StartTextDetection()
    analyzer.GetTextDetectionResults()

    return {
        'statusCode': 200,
        'body': json.dumps('Video analysis completed!')
    }
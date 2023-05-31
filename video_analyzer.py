from license_plate_validator import LicensePlateValidator
from s3_saver import S3Saver
from datetime import timedelta
from rekognition_service import RekognitionService



class VideoAnalyzer:
    def __init__(self, role_arn, bucket, video):
        self.roleArn = role_arn
        self.bucket = bucket
        self.video = video
        self.results = {}

    def start_text_detection(self):
        rekognition_service = RekognitionService()
        response = rekognition_service.start_text_detection(self.video)
        self.startJobId = response['JobId']
        print('Start Job Id: ' + self.startJobId)

    def process_license_plate(self, license_plate, timestamp):
        current_time = str(timedelta(milliseconds=timestamp))
        if license_plate in self.results:
            self.results[license_plate].append(current_time)
        else:
            self.results[license_plate] = [current_time]

    def get_text_detection_results(self):
        rekognition_service = RekognitionService()
        pagination_token = ''
        finished = False
        while not finished:
            response = rekognition_service.get_text_detection_results(self.startJobId, pagination_token)
            if response['JobStatus'] == "IN_PROGRESS":
                continue
            else:
                license_plate_validator = LicensePlateValidator()
                s3_saver = S3Saver()
                for detection in response['TextDetections']:
                    detected_text = detection['TextDetection']['DetectedText']
                    timestamp = detection['Timestamp']
                    if license_plate_validator.validate_license_plate(detected_text):
                        self.process_license_plate(detected_text, timestamp)
                        print(detected_text)
                        print(timestamp)

                s3_saver.save_data_s3(self.bucket, self.results)
                finished = True
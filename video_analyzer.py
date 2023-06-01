from license_plate_validator import LicensePlateValidator
from s3_saver import S3Saver
from datetime import timedelta
from datetime import datetime
from rekognition_service import RekognitionService
import logging




class VideoAnalyzer:
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    def __init__(self, role_arn, bucket, video):
        self.roleArn = role_arn
        self.bucket = bucket
        self.video = video
        self.results = []


    def start_text_detection(self):
        rekognition_service = RekognitionService()
        response = rekognition_service.start_text_detection(self.video)
        self.startJobId = response['JobId']
        logging.info('Start Job Id: ' + self.startJobId)



    def get_license_plate_results(self):
        rekognition_service = RekognitionService()
        pagination_token = ''
        finished = False
        while not finished:
            response = rekognition_service.get_text_detection_results(self.startJobId, pagination_token)
            if response['JobStatus'] == "SUCCEEDED":
                self.handle_successful_response(response)
                if 'NextToken' in response:
                    pagination_token = response['NextToken']
                else:
                    s3_saver = S3Saver()
                    s3_saver.save_data_s3(self.bucket, self.results)
                    logging.info('Detection finished')
                    finished = True
            else:
                continue


    def handle_successful_response(self, response):
        license_plate_validator = LicensePlateValidator()
        for detection in response['TextDetections']:
            detected_text = detection['TextDetection']['DetectedText']
            timestamp = detection['Timestamp']
            if license_plate_validator.validate_license_plate(detected_text):
                self.process_license_plate(detected_text, timestamp)
                logging.info('Detected license plates: ' + detected_text)



    def process_license_plate(self, license_plate, timestamp):
        current_time = datetime.fromtimestamp(timestamp / 1000.0)
        found_plate = False

        for result in self.results:
            if result['license_plate'] == license_plate:
                last_segment = result['video_segments'][-1]
                end_time = last_segment['end_time']
                time_diff = current_time - end_time
                if time_diff <= timedelta(seconds=10):
                    last_segment['end_time'] = current_time
                    logging.info(f"Changed segment end time: {license_plate}")
                else:
                    result['video_segments'].append({
                        'start_time': current_time,
                        'end_time': current_time
                    })
                    logging.info(f"Added new segment: {license_plate}")

                found_plate = True
                break

        if not found_plate:
            self.results.append({
                'license_plate': license_plate,
                'video_segments': [{
                    'start_time': current_time,
                    'end_time': current_time
                }]
            })
            logging.info(f"Added new license plate: {license_plate}")

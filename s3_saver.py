import boto3
import json
import logging

class S3Saver:
    def save_data_s3(self, bucket, results):
        logger = logging.getLogger()
        logger.setLevel(logging.INFO)
        s3 = boto3.resource('s3')
        json_data = []
        for result in results:
            license_plate = result['license_plate']
            video_segments = result['video_segments']
            segment_list = []
            for segment in video_segments:
                start_time = segment['start_time'].strftime('%H:%M:%S.%f')[:-3]
                end_time = segment['end_time'].strftime('%H:%M:%S.%f')[:-3]
                segment_data = {
                    'start_time': start_time,
                    'end_time': end_time
                }
                segment_list.append(segment_data)
                
            result_data = {
                'license_plate': license_plate,
                'video_segments': segment_list
            }
            json_data.append(result_data)

        s3.Object(bucket, 'output.json').put(Body=json.dumps(json_data))
        logging.info('Data saved in S3')
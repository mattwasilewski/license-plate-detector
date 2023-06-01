import json
from video_analyzer import VideoAnalyzer

def lambda_handler(event, context):
    role_arn = event['role']
    bucket = event['bucket']
    video = {
        'bucket': bucket,
        'file': event['file']
    }
    analyzer = VideoAnalyzer(role_arn, bucket, video)
    analyzer.start_text_detection()
    analyzer.get_license_plate_results()

    return {
        'statusCode': 200,
        'body': json.dumps('Video analysis completed!')
    }
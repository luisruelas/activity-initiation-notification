import json
import os
import boto3
from code.helpers.database_helper import DatabaseHelper
from code.helpers.elastic_helper import ElasticSearchHelper


NOTIFICATIONS = {
    "en": {
        "title": "Step by step… oh baby 🎶",
        "body": "You’ve started moving — and Vivanta’s keeping count. Tap to see your progress."
    },
    "es": {
        "title": "Pasito a pasito, suave, suavecito 🎶",
        "body": "Hoy ya te moviste — y Vivanta está contando cada paso. Toca para ver tu progreso."
    }
}

def lambda_handler(event, context): # pylint: disable=unused-argument
    application_identifiers = DatabaseHelper().get_application_identifiers_created_yesterday()
    vivanta_user_ids = [identifier.user_id for identifier in application_identifiers]
    user_ids_with_steps = ElasticSearchHelper.get_users_ids_with_steps(vivanta_user_ids)
    # get application identifiers with steps
    application_identifiers_with_steps = [
        identifier for identifier in application_identifiers if identifier.user_id in user_ids_with_steps
    ]
    sqs = boto3.client('sqs', region_name=os.environ.get('AWS_REGION'))
    for identifier in application_identifiers_with_steps:
        language = identifier.language
        notification_title = NOTIFICATIONS[language]["title"]
        notification_body = NOTIFICATIONS[language]["body"]
        push_id = identifier.push_id
        message_body = {
            "notificationTitle": notification_title,
            "notificationBody": notification_body,
            "data": {
                "screen": "/graphs/activity_elastic"
            },
            "isSilent": False,
            "deviceTokens": [push_id],
            "notificationId": os.environ.get('NOTIFICATION_ID'),
            "language": language,
        }
        if os.environ.get('ENV') == 'local':
            print('message_body', message_body)
        elif os.environ.get('ENV') == 'stg' and str(identifier.user_id) in os.environ.get('VIVANTA_USER_IDS').split("|"):
            response = sqs.send_message(
                QueueUrl=os.environ.get('FIREBASE_SEND_QUEUE_URL'),
                MessageBody=json.dumps(message_body)
            )
            print(f'response for user {identifier.user_id}: ', response)
        elif os.environ.get('ENV') == 'production':
            response = sqs.send_message(
                QueueUrl=os.environ.get('FIREBASE_SEND_QUEUE_URL'),
                MessageBody=json.dumps(message_body)
            )
            print(f'response for user {identifier.user_id}: ', response)

    return {
        'statusCode': 200,
        'body': 'hello lambda'
    }

import datetime
import json
import os
import boto3
from code.helpers.database_helper import ApplicationIdentifier, DatabaseHelper

NOTIFICATIONS = {
    "en": [
        {
            "title": "Just checking on you 🏃",
            "body": "Tap to see how your activity looks today",
            "min": 0,
            "max": 499
        },
        {
            "title": "Still under 7,000 steps today 😓",
            "body": "You’ve got time — a bit more movement today can get you into the moderate zone.",
            "min": 500,
            "max": 6999
        },
        {
            "title": "You’ve hit 7,000+ steps today 🔥 👟",
            "body": "That’s moderate activity — nice job staying active. Tap to see your day so far.",
            "min": 7000,
            "max": 9999
        },
        {
            "title": "You’ve passed 10,000 steps today 🔥 👟",
            "body": "That’s a big win. Your activity today leads the way — tap to review your progress.",
            "min": 10000,
            "max": 500000
        }
    ],
    "es": [
        {
            "title": "Checando checando  🏃",
            "body": "Toca para ver cómo va tu actividad hoy",
            "min": 0,
            "max": 499
        },
        {
            "title": "Aún estás por debajo de 7,000 pasos hoy 😓",
            "body": "Registrar tu sueño ahora te ayuda a entender tus hábitos. Toca para registrarlo.",
            "min": 0,
            "max": 6999
        },
        {
            "title": "Hoy pasaste los 7,000 pasos 🔥 👟",
            "body": "Eso es actividad moderada — buen trabajo manteniéndote en movimiento. Toca para ver tu día.",
            "min": 7000,
            "max": 9999
        },
        {
            "title": "Hoy pasaste los 10,000 pasos 🔥 👟",
            "body": "¡Gran logro! Tu actividad de hoy marca la diferencia. Toca para ver tu avance.",
            "min": 10000,
            "max": 500000
        }
    ]
}
DAYS_BEFORE_CHECK = 4
def lambda_handler(event, context): # pylint: disable=unused-argument
    application_identifiers = DatabaseHelper().get_possible_application_identifiers()
    
    lambdas = boto3.client('lambda', region_name='us-east-1')

    sqs = boto3.client('sqs', region_name=os.environ.get('AWS_REGION'))
    for identifier in application_identifiers:
        identifier_list= list(identifier)
        identifier: ApplicationIdentifier = identifier_list[0]
        brand_id = identifier_list[1]
        if identifier.push_id is None or identifier.push_id == '':
            print(f'No push_id for user {identifier.user_id}')
            continue
        now = datetime.datetime.now()
        now_in_utc = datetime.datetime.now(datetime.timezone.utc)
        now_in_utc: str = now_in_utc.strftime("%Y-%m-%dT%H:%M:%S")
        user_timezone_offset = identifier.timezone_offset or -6
        now_in_user_local_time = now + datetime.timedelta(hours=user_timezone_offset)
        now_in_user_local_time: str = now_in_user_local_time.strftime("%Y-%m-%dT%H:%M:%S")
        days_before_start = now - datetime.timedelta(days=DAYS_BEFORE_CHECK)
        days_before_start: str = days_before_start.strftime("%Y-%m-%dT%H:%M:%S")
        response = lambdas.invoke(
            FunctionName=os.environ.get('READ_ELASTIC'),
            Payload=json.dumps({
                "user_id": identifier.user_id,
                "brand_id": brand_id,
                "date_from": days_before_start,
                "date_to": now_in_utc,
                "parameter_catalog_id": 1,
                "hours_utc_offset": -6,
            })
        )
        payload = json.loads(response['Payload'].read())
        body = payload.get('body')
        if len(body) == 0:
            print(f'No steps in the last {DAYS_BEFORE_CHECK} days for user {identifier.user_id}')
            continue
        else:
            # get steps for yyyy-mm-dd which is in date
            steps_object_today = body[-1]
            if steps_object_today.get('date') != now_in_user_local_time[0:10]:
                print(f'Steps for {now_in_user_local_time[0:10]} not found for user {identifier.user_id}')
                continue
            steps_today = steps_object_today.get('value')
            for evaluating_notification in NOTIFICATIONS[identifier.language]:
                if steps_today >= evaluating_notification["min"] and steps_today <= evaluating_notification["max"]:
                    notification = evaluating_notification
                    break
        language = identifier.language
        notification_title = notification["title"]
        notification_body = notification["body"]
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
            'tone': 'rogerian'
        }
        if os.environ.get('ENV') == 'local':
            print(f'response for user {identifier.user_id}: ', body)
            pass
        if os.environ.get('ENV') == 'stg':
            print(f'STG response for user {identifier.user_id}')
        if os.environ.get('ENV') == 'stg' and str(identifier.user_id) in os.environ.get('VIVANTA_USER_IDS').split("|"):
            response = sqs.send_message(
                QueueUrl=os.environ.get('FIREBASE_SEND_QUEUE_URL'),
                MessageBody=json.dumps(message_body)
            )
        if os.environ.get('ENV') == 'production':
            response = sqs.send_message(
                QueueUrl=os.environ.get('FIREBASE_SEND_QUEUE_URL'),
                MessageBody=json.dumps(message_body)
            )
            print(f'response for user {identifier.user_id}: ', response)

    return {
        'statusCode': 200,
        'body': 'hello lambda'
    }

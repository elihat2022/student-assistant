import io
import os
from typing import List, Union

from celery import shared_task
from celery.exceptions import Ignore
from decouple import config
from django.conf import settings
from openai import OpenAI
from pydantic import BaseModel
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

from .models import Keywords, Transcription

client = OpenAI(api_key=settings.OPENAI_API_KEY)

# tasks.py


@shared_task(bind=True, max_retries=3)
def transcribe_audio(self, audio_path, transcription_id):
    try:
        with open(audio_path, "rb") as audio_file:
            audio_bytes = io.BytesIO(audio_file.read())
            audio_bytes.name = os.path.basename(audio_path)

            transcript_object = client.audio.transcriptions.create(
                model="whisper-1",
                file=audio_bytes,
                language="en",
            )

            transcription_text = transcript_object.text

            try:
                transcription = Transcription.objects.get(pk=transcription_id)
            except Transcription.DoesNotExist:
                raise Ignore()

            # Save the transcription text to the database
            transcription.transcription = transcription_text
            transcription.save()

            # Call the next task
            assistant.delay(transcription_text, transcription_id)

            send_email.delay(transcription_id)

            return transcription_text
    except Exception as e:
        self.retry(exc=e, countdown=2**self.request.retries)
        return f"Error al transcribir: {str(e)}"

class KeywordsData(BaseModel):
    treatment_description: str


class KeywordsResume(BaseModel):
    Topic: str
    description: str
    highlights: List[Union[KeywordsData, str]]

    class Config:
        json_schema_extra = {
            "example": {
                "topic": "Simple present",
                "description": "English class about simple present",
                "highlights": [
                    "Simple Present",
                ],
            }
        }


@shared_task(bind=True, max_retries=3)
def assistant(self, transcription, transcription_id):
    try:
        completion = client.beta.chat.completions.parse(
            model="gpt-4o",
            messages=[
                {
                    "role": "developer",
                    "content": "You are an expert at structured data extraction and student assistant. You will be given unstructured text from, please respond creating only a json format with this fields: 'topic': title of the topic, 'description': description of the class or topic, 'highlights': list of highlights useful for the student, please don't include ```json tags, in addition use only the context, if you don't have some information in the context just fill with 'No provided'",
                },
                {
                    "role": "user",
                    "content": transcription,
                },
            ],
            response_format=KeywordsResume,
        )

        message = completion.choices[0].message.parsed

        try:
            transcription = Transcription.objects.get(pk=transcription_id)
        except Transcription.DoesNotExist:
            raise Ignore()

        transcription.name = message.Topic
        transcription.description = message.description
        transcription.save()

        # Create associated Keywords instances
        highlights = message.highlights or []
        for highlight in highlights:
            Keywords.objects.create(
                transcription_record=transcription, description=highlight
            )

        return message.model_dump()
    except Exception as e:
        self.retry(exc=e, countdown=2**self.request.retries)
        return f"Error al resumir: {str(e)}"


@shared_task
def send_email(transcription_id):
    transcription = Transcription.objects.get(pk=transcription_id)
    student = transcription.student
    user = student.user
    email = user.email
    message = Mail(
        from_email=config("SENDGRID_SENDER_EMAIL"),
        to_emails=email,
        subject="Transcription Completed",
        html_content=f"<strong> Hi {user.get_full_name()}, Your transcription is ready!",
    )
    try:
        sg = SendGridAPIClient(config("SENDGRID_API_KEY"))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e.message)

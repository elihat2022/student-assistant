from django.db import models
from django.utils import timezone
# Create your models here.
from django.urls import reverse
from taggit.managers import TaggableManager


class Subject(models.Model):
    subject_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.subject_name}"


class Keywords(models.Model):
    transcription_record = models.ForeignKey(
        "Transcription", on_delete=models.CASCADE, related_name="treatments"
    )
    description = models.TextField()

    def __str__(self):
        return self.description


class Transcription(models.Model):
    student = models.ForeignKey("account.Student", on_delete=models.CASCADE)
    audio = models.FileField(upload_to="audios/")
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    subject = models.ForeignKey(
        Subject, on_delete=models.CASCADE, related_name="Transcription"
    )
    transcription = models.TextField()

    name = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    tags = TaggableManager()
    
    
    class Meta:
        ordering = ["-publish"]
        indexes = [models.Index(fields=['-publish'])]
    def __str__(self):
        return f"Transcription {self.id}"
    # def get_absolute_url(self):
    #     return reverse(
    #         "blog:post_detail",
    #         args=[self.publish.year, self.publish.month, self.publish.day, self.slug],
    #     )
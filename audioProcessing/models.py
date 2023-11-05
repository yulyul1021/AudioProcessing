from django.db import models


class AudioData(models.Model):
    create_date = models.DateTimeField()
    original_video = models.FileField(upload_to='vidio/original/', null=True, blank=True)
    original_audio = models.FileField(upload_to='audio/original/', null=True, blank=True)

    original_text = models.TextField(blank=True)
    processed_text = models.TextField(blank=True)
    processed_audio = models.FileField(upload_to='audio/processed/')
    onset = models.FloatField(blank=True)
    offset = models.FloatField(blank=True)
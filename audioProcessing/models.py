from django.db import models


class AudioData(models.Model):
    create_date = models.DateTimeField()
    original_audio = models.FileField(upload_to='original/', null=True, blank=True)
    original_text = models.TextField(blank=True)
    processed_text = models.TextField(blank=True)
    processed_audio = models.FileField(upload_to='processed/')
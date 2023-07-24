from django.db import models


class AudioData(models.Model):
    original_audio = models.FileField(upload_to='original/')
    original_text = models.TextField()
    create_date = models.DateTimeField()
    processed_text = models.TextField()
    processed_audio = models.FileField(upload_to='processed/')
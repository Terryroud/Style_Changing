from django.db import models
import os
import uuid

def get_upload_path(instance, filename):
    return os.path.join('uploads', str(uuid.uuid4()), filename)

class StyleTransferResult(models.Model):
    content_image = models.ImageField(upload_to=get_upload_path)
    style_image = models.ImageField(upload_to=get_upload_path)
    result_image = models.ImageField(upload_to='results/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Style transfer result {self.id}"
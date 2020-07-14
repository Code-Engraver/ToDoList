from django.db import models


class Todo(models.Model):
    content = models.CharField(max_length=255)
    is_done = models.BooleanField(default=False)

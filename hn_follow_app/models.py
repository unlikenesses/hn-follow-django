from django.db import models

class HnUser(models.Model):
    username = models.CharField(max_length=200)

    def __str__(self):
        return self.username
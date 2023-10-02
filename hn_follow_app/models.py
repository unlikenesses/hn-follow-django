from django.db import models

class HnUser(models.Model):
    username = models.CharField(max_length=200)
    about = models.TextField(null=True)
    karma = models.IntegerField(null=True)
    submissions = models.JSONField(null=True)
    notes = models.TextField(null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.username
    
class HnSubmission(models.Model):
    id = models.IntegerField(null=False, primary_key=True)
    text = models.TextField(null=True)
    time = models.IntegerField(null=False)
    type = models.CharField(max_length=16, null=False)
    by = models.CharField(max_length=200, null=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.text is None:
            text = ''
        else:
            text = self.text[:50]
        return str(self.id)+': '+text+' ('+self.by+')'
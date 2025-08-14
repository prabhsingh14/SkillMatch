from django.db import models

# Create your models here.
class Skill(models.Model):
    name = models.CharField(unique=True, max_length=100)

    def __str__(self):
        
        return self.name

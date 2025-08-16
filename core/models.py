from django.db import models

# Create your models here.
class Skill(models.Model):
    name = models.CharField(unique=True, max_length=100)
    category = models.CharField(max_length=50, choices=[
        ('technical', 'Technical'),
        ('soft', 'Soft'),
        ('other', 'Other')
    ], default='technical')

    def __str__(self):
        
        return self.name

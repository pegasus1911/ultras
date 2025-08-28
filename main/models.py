from django.db import models

class Group(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)   
    founding_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

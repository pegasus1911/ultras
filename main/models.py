from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

TIFO_TYPES = (
    ('C', 'Choreo'),
    ('P', 'Pyro Show'),
    ('B', 'Banner'),
)

class Group(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)   
    founding_year = models.IntegerField()
    description = models.TextField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'group_id': self.id})


class Tifo(models.Model):
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    date = models.DateField('Tifo date')
    match = models.CharField(max_length=200, default=' ')
    description = models.TextField()
    picture = models.ImageField(upload_to='tifos/', blank=True, null=True)

    def __str__(self):
        return f"{self.group.name} Tifo on {self.date} for {self.match}"

    class Meta:
        ordering = ['-date']  # newest tifos show up first

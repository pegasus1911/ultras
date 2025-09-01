from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
TIFO_TYPES = (
    ('C', 'Choreo'),
    ('P', 'Pyro Show'),
    ('B', 'Banner'),
)

class Country(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name

class Group(models.Model):
    name = models.CharField(max_length=100)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, related_name='groups')
    founding_year = models.IntegerField()
    description = models.TextField()
    logo = models.ImageField(upload_to='group_logos/', null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('group-detail', kwargs={'group_id': self.id})

class Tifo(models.Model):
    date = models.DateField('Tifo date')
    tifo_type = models.CharField(
        max_length=1,
        choices=TIFO_TYPES,
        default=TIFO_TYPES[0][0]
    )
    description = models.TextField()
    picture = models.ImageField(upload_to='tifos/', null=True, blank=True)
    match = models.CharField(max_length=200, default="Unknown match")  
    group = models.ForeignKey(Group, on_delete=models.CASCADE)
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.get_tifo_type_display()} on {self.date}"

    class Meta:
        ordering = ['-date']


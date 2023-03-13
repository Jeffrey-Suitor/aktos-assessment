from django.db import models


# Create your models here.
class Consumer(models.Model):
    class Meta:
        ordering = ['id']
    
    STATUS = ['active', 'in_progress', 'collected']
    
    id = models.IntegerField(primary_key=True)
    street = models.CharField(max_length=200)
    status = models.CharField(max_length=20, choices=[(x, x) for x in STATUS])
    previous_jobs_count = models.IntegerField()
    amount_due = models.IntegerField()
    lat = models.FloatField()
    lng = models.FloatField()
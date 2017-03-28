from django.db import models
from django.utils import timezone

# Create your models here.
class Collision(models.Model):
    hash_order = models.IntegerField()
    input_hash = models.CharField(max_length=30)
    total_time = models.CharField(max_length=30)
    cycles = models.IntegerField()
    coll_hash = models.CharField(max_length=30)
    test_method = models.CharField(max_length=30)
    bits = models.IntegerField()
    git_revision = models.CharField(max_length=50)


from django.db import models
from django.utils import timezone


class Collision(models.Model):
    hash_order = models.IntegerField() #indexOfLast
    input_hash = models.CharField(max_length=60) #inputHash
    total_time = models.FloatField()    #time
    cycles = models.IntegerField()      #cyclesBetCol
    coll_hash = models.CharField(max_length=60) #collisionHash
    firstTemp = models.CharField(default=0, max_length=60) #first temp
    lastTemp = models.CharField(default=0, max_length=60)  #last temp
    total_memory = models.FloatField(default=0.0) #dataStructConsum
    test_method = models.CharField(max_length=30)   #method
    bits = models.IntegerField()    #bits
    git_revision = models.CharField(max_length=30)  #git_repo.git.describe()

    def publish(self):
        self.save()

    def __str__(self):
        return (self.input_hash)

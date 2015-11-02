from django.db import models

NETWORK_CHOICES = {
    ('PSN', 'Playstation Network'),
    ('S', 'Steam'),
}

# Create your models here.
class RLUser(models.Model):
    display_name = models.CharField(max_length=75)
    network = models.CharField(max_length=3, choices=NETWORK_CHOICES)
    network_id = models.BigIntegerField(null=True, blank=True)

class RLSkills(models.Model):
    wins = models.IntegerField()
    goals = models.IntegerField()
    mvps = models.IntegerField()
    saves = models.IntegerField()
    shots = models.IntegerField()
    assists = models.IntegerField()
    user = models.OneToOneField(RLUser)

class RLSkillsHistorical(models.Model):
    wins = models.IntegerField()
    goals = models.IntegerField()
    mvps = models.IntegerField()
    saves = models.IntegerField()
    shots = models.IntegerField()
    assists = models.IntegerField()
    user = models.ForeignKey(RLUser)
    date = models.DateTimeField() 

class RLRatings(models.Model):
    user = models.OneToOneField(RLUser)
    mt_1v1 = models.IntegerField()
    mt_2v2 = models.IntegerField()
    mt_3v3_solo = models.IntegerField()
    mt_3v3 = models.IntegerField()

class RLRatingsHistorical(models.Model):
    user = models.ForeignKey(RLUser)
    mt_1v1 = models.IntegerField()
    mt_2v2 = models.IntegerField()
    mt_3v3_solo = models.IntegerField()
    mt_3v3 = models.IntegerField()
    date = models.DateTimeField()

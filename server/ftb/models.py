from django.db import models
from choices import VISUAL_LOSS_AGE_CHOICES, GENDER_CHOICES
from locking.models import LockableModel

class Patient(LockableModel):
    name = models.CharField('Name', max_length=50, db_index=True)

class PatientDetails(models.Model):
    ethnic_group = models.CharField('Ethnic group', max_length=50)
    age = models.IntegerField('Age')
    sex = models.CharField('Sex', max_length=1, choices=GENDER_CHOICES)
    visual_loss_age = models.IntegerField('Age at onset of visual loss', max_length=2, choices=VISUAL_LOSS_AGE_CHOICES)
    patient = models.OneToOneField(Patient, related_name='details')
    
    def __unicode__(self):
        return self.patient.name
    
class Address(models.Model):
    town = models.CharField('Town/Village', max_length=50, db_index=True)
    patient = models.OneToOneField(Patient, related_name='address')
    
    def __unicode__(self):
        return self.patient.name

class FamilyHistory(models.Model):
    has_family_history = models.NullBooleanField('Is there a famliy history for same reason')
    affected_relation = models.CharField('Who is affected?', null=True, blank=True)
    consanguinity = models.NullBooleanField('Is there history of consanguinity')
    



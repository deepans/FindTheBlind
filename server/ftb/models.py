import ftb.signals
from django.db import models
from choices import VISUAL_LOSS_AGE_CHOICES, GENDER_CHOICES
from locking.models import LockableModel
from ftb.mixins import ConcurrentlyModifiable, JsonEncodable
from django.core.exceptions import ValidationError

class Patient(LockableModel, ConcurrentlyModifiable, JsonEncodable):
    name = models.CharField('Name', max_length=50, db_index=True)

class PatientDetails(ConcurrentlyModifiable):
    ethnic_group = models.CharField('Ethnic group', max_length=50)
    age = models.IntegerField('Age')
    sex = models.CharField('Sex', max_length=1, choices=GENDER_CHOICES)
    visual_loss_age = models.IntegerField('Age at onset of visual loss', max_length=2, choices=VISUAL_LOSS_AGE_CHOICES)
    patient = models.OneToOneField(Patient, related_name='details')
    
class Address(ConcurrentlyModifiable):
    town = models.CharField('Town/Village', max_length=50, db_index=True)
    patient = models.OneToOneField(Patient, related_name='address')
    
class FamilyHistory(ConcurrentlyModifiable):
    has_family_history = models.NullBooleanField('Is there a famliy history for same reason')
    affected_relation = models.CharField('Who is affected?', max_length=250, null=True, blank=True)
    consanguinity = models.NullBooleanField('Is there history of consanguinity')
    patient = models.OneToOneField(Patient, related_name='family_history')
    
    def clean(self):
        if not self.has_family_history and (self.affected_relation or self.consanguinity):
            raise ValidationError("Should'nt has_family_history is true?")
    



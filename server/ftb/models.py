import ftb.signals
from django.db import models
from choices import VISUAL_LOSS_AGE_CHOICES, GENDER_CHOICES
from locking.models import LockableModel
from ftb.mixins import ConcurrentlyModifiable
from json.mixins import JsonEncodable
from django.core.exceptions import ValidationError

class Patient(LockableModel, ConcurrentlyModifiable, JsonEncodable):
    name = models.CharField('Name', max_length=250, db_index=True)
    relations_included_in_json = ('patientdetails', 'address', 'familyhistory')

class PatientDetails(ConcurrentlyModifiable):
    ethnic_group = models.CharField('Ethnic group', max_length=250)
    date_of_birth = models.DateField('Date of birth')
    age = models.IntegerField('Age', max_length=2)
    sex = models.CharField('Sex', max_length=1, choices=GENDER_CHOICES)
    fathers_name = models.CharField("Father's name", max_length=250)
    fathers_phone_number = models.IntegerField("Father's phone number'", max_length=12)
    mothers_name = models.CharField("Mother's name'", max_length=250)
    mothers_phone_number = models.IntegerField("Mother's phone number'", max_length=12)
    guardians_name = models.CharField("Guardian's name'", max_length=250)
    guardians_phone_number = models.IntegerField("Guardian's phone number'", max_length=12)
    health_workers_name = models.CharField("Health worker's name'", max_length=250)
    health_workers_phone_number = models.IntegerField("Health worker's phone number'", max_length=12)
    visual_loss_age = models.IntegerField('Age at onset of visual loss', max_length=2, choices=VISUAL_LOSS_AGE_CHOICES)
    patient = models.OneToOneField(Patient, related_name='patientdetails')

class Address(ConcurrentlyModifiable):
    town = models.CharField('Town/Village', max_length=250, db_index=True)
    patient = models.OneToOneField(Patient, related_name='address')
    
class FamilyHistory(ConcurrentlyModifiable):
    has_family_history = models.NullBooleanField('Is there a famliy history for same reason')
    affected_relation = models.CharField('Who is affected?', max_length=250, null=True, blank=True)
    consanguinity = models.NullBooleanField('Is there history of consanguinity')
    patient = models.OneToOneField(Patient, related_name='familyhistory')
    
    def clean(self):
        if not self.has_family_history and (self.affected_relation or self.consanguinity):
            raise ValidationError("Should'nt has_family_history be true?")
    



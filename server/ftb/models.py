from django.db import models

GENDER_CHOICES = (
    ('M', 'Male'),
    ('F', 'Female'),
)

class Patient(models.Model):
    name = models.CharField('Name', max_length=50, db_index=True)

class PatientDetails(models.Model):
    VISUAL_LOSS_AGE_CHOICES = (
        (00, 'Since Birth'),
        (88, 'First Year of life'),
        (99, 'Unknown')
    ) + tuple(zip(range(1, 15), ("{0} in Years".format(years) for years in range(1, 15))))
    
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




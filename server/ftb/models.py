from django.db import models

class Patient(models.Model):
    name = models.CharField('Name', max_length=250, db_index=True)
    fathers_name = models.CharField('Fathers Name', max_length=250)

    @staticmethod
    def save_or_update(**kwargs):
        pass
            
        

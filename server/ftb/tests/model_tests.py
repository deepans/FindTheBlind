from django.test import TestCase
from ftb.models import FamilyHistory, PatientDetails, Patient, Address
from ftb.model_factory import FamilyHistoryFactory, PatientFactory
from ftb.tests import test_utils
from server.json.persister import ReplaceLatestMergeStrategy, persist
from django.core.exceptions import ValidationError
import simplejson

class PatientTest(TestCase):

    def test_should_encode_all_patients_in_db_to_json_string(self):
        self.assertEquals('[]', Patient.json_encode_all_entities())
        
        patient = PatientFactory.create_related()
        patient.name = 'Zeon'
        patient.save()

        details = PatientDetails.objects.filter(patient=patient)
        details[0].fathers_name = 'Mohan'
        details[0].mothers_phone_number = 9500011111
        details[0].save()

        PatientFactory.create_related()
        expected_json = '[{"patientdetails": {"patient": 3, "version": 1, "mothers_name": "Sita", "fathers_phone_number": "9520012200", ' +\
                               '"date_of_birth": "2011-01-31", "guardians_name": "John", "guardians_phone_number": "9520012222", ' +\
                               '"health_workers_phone_number": "9520012233", "ethnic_group": "Hindu", "mothers_phone_number": "9520012211", ' +\
                               '"gender": "M", "age": 29, "health_workers_name": "Ahmad", "fathers_name": "Ramanan", ' +\
                               '"visual_loss_age": 99, "pk": 1, "model": "ftb.patientdetails"}, ' +\
                        '"_locked_by": null, "_hard_lock": false, "version": 1, ' +\
                        '"familyhistory": {"has_family_history": true, "version": 1, "patient": 3, "affected_relation": "Uncle", "pk": 2, ' +\
                               '"model": "ftb.familyhistory", "consanguinity": false}, ' +\
                        '"address": {"town": "Neyveli", "pk": 1, "model": "ftb.address", "version": 1, "patient": 3}, ' +\
                        '"_locked_at": null, "pk": 3, "model": "ftb.patient", "name": "Zeon"}, ' +\
                        '{"patientdetails": {"patient": 4, "version": 1, "mothers_name": "Sita", "fathers_phone_number": "9520012200", ' +\
                               '"date_of_birth": "2011-01-31", "guardians_name": "John", "guardians_phone_number": "9520012222", ' +\
                               '"health_workers_phone_number": "9520012233", "ethnic_group": "Hindu", "mothers_phone_number": "9520012211", '+\
                               '"gender": "M", "age": 29, "health_workers_name": "Ahmad", "fathers_name": "Ramanan", '+\
                               '"visual_loss_age": 99, "pk": 2, "model": "ftb.patientdetails"}, ' +\
                        '"_locked_by": null, "_hard_lock": false, "version": 1, ' +\
                        '"familyhistory": {"has_family_history": true, "version": 1, "patient": 4, "affected_relation": "Uncle", "pk": 3, ' +\
                               '"model": "ftb.familyhistory", "consanguinity": false}, ' +\
                        '"address": {"town": "Neyveli", "pk": 2, "model": "ftb.address", "version": 1, "patient": 4}, ' +\
                        '"_locked_at": null, "pk": 4, "model": "ftb.patient", "name": "Arjun"}]'

        self.assertEquals(simplejson.loads(expected_json), simplejson.loads(Patient.json_encode_all_entities()))

    def test_should_serialize_patient_objects_from_json(self):
        test_utils.set_sequence([Patient, PatientDetails, Address, FamilyHistory])
        self.assertEquals(0, Patient.objects.count())
        self.assertEquals(0, PatientDetails.objects.count())
        self.assertEquals(0, Address.objects.count())
        self.assertEquals(0, FamilyHistory.objects.count())
        
        json = '[{"patientdetails": {"patient": 1, "version": 1, "mothers_name": "Sita", "fathers_phone_number": "9520012200", ' +\
                        '"date_of_birth": "2011-01-31", "guardians_name": "John", "guardians_phone_number": "9520012222", ' +\
                        '"health_workers_phone_number": "9520012233", "ethnic_group": "Hindu", "mothers_phone_number": "9520012211", ' +\
                        '"gender": "M", "age": 29, "health_workers_name": "Ahmad", "fathers_name": "Ramanan", "visual_loss_age": 99, "pk": 1,' +\
                        '"model": "ftb.patientdetails"}, ' +\
                   '"_locked_by": null, "_hard_lock": false, "version": 1, ' +\
                   '"familyhistory": {"has_family_history": true, "version": 1, "patient": 1, "affected_relation": "Uncle", "pk": 1, ' +\
                        '"model": "ftb.familyhistory", "consanguinity": false}, ' +\
                   '"address": {"town": "Neyveli", "pk": 1, "model": "ftb.address", "version": 1, "patient": 1}, ' +\
                   '"_locked_at": null, "pk": 1, "model": "ftb.patient", "name": "Zeon"}, ' +\
                   '{"patientdetails": {"patient": 2, "version": 1, "mothers_name": "Sita", "fathers_phone_number": "9520012200", ' +\
                        '"date_of_birth": "2011-01-31", "guardians_name": "John", "guardians_phone_number": "9520012222", ' +\
                        '"health_workers_phone_number": "9520012233", "ethnic_group": "Hindu", "mothers_phone_number": "9520012211", ' +\
                        '"gender": "M", "age": 29, "health_workers_name": "Ahmad", "fathers_name": "Ramanan", "visual_loss_age": 99, "pk": 2, ' +\
                        '"model": "ftb.patientdetails"}, ' +\
                   '"_locked_by": null, "_hard_lock": false, "version": 1, ' +\
                   '"familyhistory": {"has_family_history": true, "version": 1, "patient": 2, "affected_relation": "Uncle", "pk": 2, ' +\
                        '"model": "ftb.familyhistory", "consanguinity": false}, ' +\
                   '"address": {"town": "Neyveli", "pk": 2, "model": "ftb.address", "version": 1, "patient": 2}, ' +\
                   '"_locked_at": null, "pk": 2, "model": "ftb.patient", "name": "Arjun"}]'

        persist(json, ReplaceLatestMergeStrategy)

        self.assertEquals(2, Patient.objects.count())
        self.assertEquals(2, PatientDetails.objects.count())
        self.assertEquals(2, Address.objects.count())
        self.assertEquals(2, FamilyHistory.objects.count())
        
        expected_json = '[{"patientdetails": {"patient": 1, "version": 1, "mothers_name": "Sita", "fathers_phone_number": "9520012200", ' +\
                              '"date_of_birth": "2011-01-31", "guardians_name": "John", "guardians_phone_number": "9520012222", ' +\
                              '"health_workers_phone_number": "9520012233", "ethnic_group": "Hindu", "mothers_phone_number": "9520012211", ' +\
                              '"gender": "M", "age": 29, "health_workers_name": "Ahmad", "fathers_name": "Ramanan", "visual_loss_age": 99, ' +\
                              '"pk": 1, "model": "ftb.patientdetails"}, ' +\
                        '"_locked_by": null, "_hard_lock": false, "version": 1, ' +\
                        '"familyhistory": {"has_family_history": true, "version": 1, "patient": 1, "affected_relation": "Uncle", "pk": 1, ' +\
                              '"model": "ftb.familyhistory", "consanguinity": false}, ' +\
                        '"address": {"town": "Neyveli", "pk": 1, "model": "ftb.address", "version": 1, "patient": 1}, ' +\
                              '"_locked_at": null, "pk": 1, "model": "ftb.patient", "name": "Zeon"}, ' +\
                        '{"patientdetails": {"patient": 2, "version": 1, "mothers_name": "Sita", "fathers_phone_number": "9520012200", ' +\
                              '"date_of_birth": "2011-01-31", "guardians_name": "John", "guardians_phone_number": "9520012222", ' +\
                              '"health_workers_phone_number": "9520012233", "ethnic_group": "Hindu", "mothers_phone_number": "9520012211", ' +\
                              '"gender": "M", "age": 29, "health_workers_name": "Ahmad", "fathers_name": "Ramanan", "visual_loss_age": 99, ' +\
                              '"pk": 2, "model": "ftb.patientdetails"}, ' +\
                        '"_locked_by": null, "_hard_lock": false, "version": 1, ' +\
                        '"familyhistory": {"has_family_history": true, "version": 1, "patient": 2, "affected_relation": "Uncle", "pk": 2, ' +\
                              '"model": "ftb.familyhistory", "consanguinity": false}, ' +\
                        '"address": {"town": "Neyveli", "pk": 2, "model": "ftb.address", "version": 1, "patient": 2}, ' +\
                        '"_locked_at": null, "pk": 2, "model": "ftb.patient", "name": "Arjun"}]'

        self.assertEquals(simplejson.loads(expected_json), simplejson.loads(Patient.json_encode_all_entities()))

class FamilyHistoryTest(TestCase):
    def test_should_validate_while_creating_and_updating_models(self):
        self.assertRaisesRegexp(ValidationError,
                                "Should'nt has_family_history be true?",
                                FamilyHistory.objects.create,
                                has_family_history=False,
                                affected_relation='Uncle',
                                consanguinity=False)
        
        family_history = FamilyHistoryFactory.create()

        family_history.has_family_history = False
        family_history.affected_relation = 'Uncle'
        
        self.assertRaisesRegexp(ValidationError,
                                "Should'nt has_family_history be true?",
                                FamilyHistory.concurrency.update,
                                family_history)
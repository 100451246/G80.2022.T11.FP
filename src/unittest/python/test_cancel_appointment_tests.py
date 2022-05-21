from unittest import TestCase
import os
import shutil
from freezegun import freeze_time
from uc3m_care import VaccineManager, FinalCancellationsJsonStore, VaccinationJsonStore
from uc3m_care import VaccineManagementException
from uc3m_care import JSON_FILES_PATH, JSON_FILES_RF2_PATH
from uc3m_care import AppointmentsJsonStore
from uc3m_care import PatientsJsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_RFF_PATH
from uc3m_care.storage.temp_cancellations_json_store import TempCancellationsJsonStore

date_param_ok = "2022-03-18"



class TestCancelAppointment(TestCase):
    """Class for testing get_vaccine_date"""

    @freeze_time("2022-03-08")
    def test_cancel_appointment_temporal_ok(self):
        """test ok"""
        file_test_cancel = JSON_FILES_RFF_PATH + "test_temporal_ok.json"
        file_test_new = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_temp_cancellations = TempCancellationsJsonStore()
        file_store_temp_cancellations.delete_json_file()
        file_store_final_cancellations = FinalCancellationsJsonStore()
        file_store_final_cancellations.delete_json_file()
        file_store_vaccines = VaccinationJsonStore()
        file_store_vaccines.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        my_manager.get_vaccine_date(file_test_new, date_param_ok)
        value = my_manager.cancel_appointment(file_test_cancel)
        self.assertEqual(value, "62ca69e8aad4b24d8588117e58b3524ffe18dac510306a9f2c3aeb5039f3afa6")
        # check store_date
        self.assertIsNone(file_store_date.find_item(value))
        self.assertIsNotNone(file_store_temp_cancellations.find_item(value))

    @freeze_time("2022-03-08")
    def test_cancel_appointment_final_ok(self):
        """test ok"""
        file_test_cancel = JSON_FILES_RFF_PATH + "test_final_ok.json"
        file_test_new = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_final_cancellations = FinalCancellationsJsonStore()
        file_store_final_cancellations.delete_json_file()
        file_store_temp_cancellations = TempCancellationsJsonStore()
        file_store_temp_cancellations.delete_json_file()
        file_store_vaccines = VaccinationJsonStore()
        file_store_vaccines.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        my_manager.get_vaccine_date(file_test_new, date_param_ok)
        value = my_manager.cancel_appointment(file_test_cancel)
        self.assertEqual(value, "62ca69e8aad4b24d8588117e58b3524ffe18dac510306a9f2c3aeb5039f3afa6")
        # check store_date
        self.assertIsNone(file_store_date.find_item(value))
        self.assertIsNotNone(file_store_final_cancellations.find_item(value))

    @freeze_time("2022-03-08")
    def test_cancel_appointment_date_signature_no_ok1(self):
        """Date_signature no se encuentra"""
        file_test = JSON_FILES_RFF_PATH + "test_nok_date_signature1.json"
        my_manager = VaccineManager()

        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "date_signature is not found")

    @freeze_time("2022-03-08")
    def test_cancel_appointment_date_signature_no_ok2(self):
        """Date_signature inválido"""
        file_test = JSON_FILES_RFF_PATH + "test_nok_date_signature2.json"
        my_manager = VaccineManager()


        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "date_signature format is not valid")

    @freeze_time("2022-03-08")
    def test_cancel_appointment_cancellation_type_no_ok(self):
        """Tipo de cancelación inexistente"""
        file_test = JSON_FILES_RFF_PATH + "test_nok_cancellation_type.json"
        file_test_new = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_final_cancellations = FinalCancellationsJsonStore()
        file_store_final_cancellations.delete_json_file()
        file_store_temp_cancellations = TempCancellationsJsonStore()
        file_store_temp_cancellations.delete_json_file()
        file_store_vaccines = VaccinationJsonStore()
        file_store_vaccines.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        my_manager.get_vaccine_date(file_test_new, date_param_ok)

        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "Cancellation Type is not valid")

    @freeze_time("2022-03-08")
    def test_cancel_appointment_reason_nok1(self):
        """Razón muy larga >200"""
        file_test = JSON_FILES_RFF_PATH + "test_nok_reason1.json"
        file_test_new = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_final_cancellations = FinalCancellationsJsonStore()
        file_store_final_cancellations.delete_json_file()
        file_store_temp_cancellations = TempCancellationsJsonStore()
        file_store_temp_cancellations.delete_json_file()
        file_store_vaccines = VaccinationJsonStore()
        file_store_vaccines.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        my_manager.get_vaccine_date(file_test_new, date_param_ok)

        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "Reason is not valid")

    @freeze_time("2022-03-08")
    def test_cancel_appointment_reason_nok2(self):
        """Razón demasiado corto <2"""
        file_test = JSON_FILES_RFF_PATH + "test_nok_reason1.json"
        file_test_new = JSON_FILES_RF2_PATH + "test_ok.json"
        my_manager = VaccineManager()

        # first , prepare my test , remove store patient
        file_store = PatientsJsonStore()
        file_store.delete_json_file()
        file_store_date = AppointmentsJsonStore()
        file_store_date.delete_json_file()
        file_store_final_cancellations = FinalCancellationsJsonStore()
        file_store_final_cancellations.delete_json_file()
        file_store_temp_cancellations = TempCancellationsJsonStore()
        file_store_temp_cancellations.delete_json_file()
        file_store_vaccines = VaccinationJsonStore()
        file_store_vaccines.delete_json_file()

        # add a patient in the store
        my_manager.request_vaccination_id("78924cb0-075a-4099-a3ee-f3b562e805b9",
                                          "minombre tienelalongitudmaxima",
                                          "Regular", "+34123456789", "6")
        # check the method
        my_manager.get_vaccine_date(file_test_new, date_param_ok)

        with self.assertRaises(VaccineManagementException) as c_m:
            my_manager.cancel_appointment(file_test)
        self.assertEqual(c_m.exception.message, "Reason is not valid")



import hashlib
from freezegun import freeze_time
from datetime import datetime

from uc3m_care.data.vaccination_appointment import VaccinationAppointment
from uc3m_care.storage.vaccination_json_store import VaccinationJsonStore
from uc3m_care.data.attribute.attribute_cancellation_type import CancellationType
from uc3m_care.data.attribute.attribute_phone_number import PhoneNumber
from uc3m_care.data.attribute.attribute_patient_system_id import PatientSystemId
from uc3m_care.data.attribute.attribute_date_signature import DateSignature
from uc3m_care.data.attribute.attribute_reason import Reason
from uc3m_care.data.vaccination_log import VaccinationLog
from uc3m_care.data.vaccine_patient_register import VaccinePatientRegister
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException
from uc3m_care.parser.cancellations_json_parser import CancellationsJsonParser
from uc3m_care.storage.appointments_json_store import AppointmentsJsonStore
from uc3m_care.parser.appointment_json_parser import AppointmentJsonParser
from uc3m_care.storage.temp_cancellations_json_store import TempCancellationsJsonStore
from uc3m_care.storage.final_cancellations_json_store import FinalCancellationsJsonStore


# pylint: disable=too-many-instance-attributes
class AppointmentCancellation():
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, input_file):
        self.appointment_already_cancelled(self.get_date_signature(input_file))
        self.__appointment_date = self.get_appointment_from_json(input_file).appointment_date
        self.__date_signature = self.get_appointment_from_json(input_file).date_signature
        self.__cancellation_type = self.get_cancellation_type(input_file)
        self.__reason = self.get_reason(input_file)

    @property
    def cancellation_type(self):
        return self.__cancellation_type

    @property
    def reason(self):
        return self.__reason

    def save_cancellation(self):
        """saves the appointment in the appointments store"""
        self.date_has_passed()
        self.vaccine_is_done()
        if self.__cancellation_type == "Temporal":
            cancellations_store = TempCancellationsJsonStore()
        else:
            cancellations_store = FinalCancellationsJsonStore()
        cancellations_store.add_item(self)

    def delete_appointment(self, input_file):
        appointment = self.get_appointment_from_json(input_file)
        my_store = AppointmentsJsonStore()
        my_store.delete_item(appointment)

    def date_has_passed(self):
        date = datetime.fromisoformat(self.__appointment_date)
        if date < datetime.fromisoformat(str(datetime.today().date())):
            raise VaccineManagementException("Cita antigua")

    def appointment_already_cancelled(self, date_signature):
        my_temp_store = TempCancellationsJsonStore()
        my_final_store = FinalCancellationsJsonStore()
        if my_final_store.find_item(date_signature) is not None:
            raise VaccineManagementException("Cita ya cancelada")
        if my_temp_store.find_item(date_signature) is not None:
            raise VaccineManagementException("Cita ya cancelada")

    def vaccine_is_done(self):
        my_store = VaccinationJsonStore()
        if my_store.find_item(self.__date_signature) is not None:
            raise VaccineManagementException("Vacuna ya administrada")

    def get_appointment_from_json(self, input_file):
        date_signature = self.get_date_signature(input_file)
        appointment = VaccinationAppointment.get_appointment_from_date_signature(date_signature)
        return appointment

    @staticmethod
    def get_cancellation_type(input_file):
        my_parser = CancellationsJsonParser(input_file)
        info = my_parser.json_content
        cancellation_type = info["cancellation_type"]
        return CancellationType(cancellation_type).value

    @staticmethod
    def get_reason(input_file):
        my_parser = CancellationsJsonParser(input_file)
        info = my_parser.json_content
        reason = info["reason"]
        return Reason(reason).value

    @staticmethod
    def get_date_signature(input_file):
        my_parser = CancellationsJsonParser(input_file)
        info = my_parser.json_content
        date_signature = info["date_signature"]
        return date_signature


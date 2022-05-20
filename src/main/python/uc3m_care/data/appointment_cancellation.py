import hashlib
from freezegun import freeze_time
from datetime import datetime

from uc3m_care import VaccinationAppointment
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

FECHA_ACTUAL = "2022-03-08"


# pylint: disable=too-many-instance-attributes
class AppointmentCancellation():
    """Class representing an appointment  for the vaccination of a patient"""

    def __init__(self, input_file):
        self.__appointment = self.get_appointment_from_json(input_file)
        self.__cancellation_type = self.get_cancellation_type(input_file)
        self.__reason = self.get_reason(input_file)

    def __signature_string(self):
        """Composes the string to be used for generating the key for the date"""
        return "{alg:" + self.__appointment.alg + ",typ:" + \
               self.__appointment.type + ",patient_sys_id:" + \
               self.__appointment.patient_sys_id + ",issuedate:" + \
               self.__appointment.issued_at.__str__() + \
               ",vaccinationtiondate:" + self.__appointment.appointment_date.__str__() + \
               ",reason:" + self.__reason + "}"

    @property
    def appointment(self):
        """Property that represents the guid of the patient"""
        return self.__appointment

    @property
    def cancellation_type(self):
        return self.__cancellation_type

    @property
    def reason(self):
        return self.__reason

    def save_cancellation(self):
        """saves the appointment in the appointments store"""
        if self.__cancellation_type == "Temporal":
            cancellations_store = TempCancellationsJsonStore()
        else:
            cancellations_store = FinalCancellationsJsonStore()
        cancellations_store.add_item(self.__appointment)

    def delete_appointment(self):
        my_store = AppointmentsJsonStore()
        my_store.delete_item(self.__appointment)


    @staticmethod
    def get_appointment_from_json(input_file):
        my_parser = CancellationsJsonParser(input_file)
        info = my_parser.json_content
        date_signature = info["date_signature"]
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



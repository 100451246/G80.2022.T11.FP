"""Class for attribute reason"""
from uc3m_care.data.attribute.attribute import Attribute
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


# pylint: disable=too-few-public-methods
class Reason(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_error_message = "Reason is not valid"

    def _validate(self, attr_value):
        if not isinstance(attr_value, str):
            raise VaccineManagementException(self._validation_error_message)
        if len(attr_value) <= 2 or len(attr_value) > 200:
            raise VaccineManagementException(self._validation_error_message)
        return attr_value

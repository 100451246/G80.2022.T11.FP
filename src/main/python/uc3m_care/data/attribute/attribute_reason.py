from uc3m_care.data.attribute.attribute import Attribute


# pylint: disable=too-few-public-methods
class CancellationType(Attribute):
    """Classs for the attribute PhoneNumber"""
    _validation_pattern = r"^(?=^.{1,30}$)(([a-zA-Z]+\s)+[a-zA-Z]+)$"
    _validation_error_message = "Reason is not valid"

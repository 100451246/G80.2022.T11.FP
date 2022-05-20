from uc3m_care.data.attribute.attribute import Attribute


# pylint: disable=too-few-public-methods
class CancellationType(Attribute):
    """Class for the attribute PhoneNumber"""
    _validation_pattern = r"(Temporal|Final)"
    _validation_error_message = "Cancellation Type is not valid"

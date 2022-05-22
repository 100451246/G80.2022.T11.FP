"""Subclass of JsonStore for managing the Final Cancellations store"""

from uc3m_care.storage.json_store import JsonStore
from uc3m_care.cfg.vaccine_manager_config import JSON_FILES_PATH
from uc3m_care.exception.vaccine_management_exception import VaccineManagementException


class FinalCancellationsJsonStore:
    """Implements the singleton pattern"""

    # pylint: disable=invalid-name
    class __FinalCancellationsJsonStore(JsonStore):
        """Subclass of JsonStore for managing the Appointments"""
        _FILE_PATH = JSON_FILES_PATH + "store_final_cancellations.json"
        _ID_FIELD = "_AppointmentCancellation__date_signature"
        ERROR_INVALID_APPOINTMENT_OBJECT = "Invalide cancelation object"

        def add_item(self, item):
            """Overrides the add_item method to verify the item to be stored"""
            # pylint: disable=import-outside-toplevel, cyclic-import
            from uc3m_care.data.appointment_cancellation import AppointmentCancellation
            if not isinstance(item, AppointmentCancellation):
                raise VaccineManagementException(self.ERROR_INVALID_APPOINTMENT_OBJECT)
            super().add_item(item)

    instance = None

    def __new__(cls):
        if not FinalCancellationsJsonStore.instance:
            FinalCancellationsJsonStore.instance = \
                FinalCancellationsJsonStore.__FinalCancellationsJsonStore()
        return FinalCancellationsJsonStore.instance

    def __getattr__(self, nombre):
        return getattr(self.instance, nombre)

    def __setattr__(self, nombre, valor):
        return setattr(self.instance, nombre, valor)

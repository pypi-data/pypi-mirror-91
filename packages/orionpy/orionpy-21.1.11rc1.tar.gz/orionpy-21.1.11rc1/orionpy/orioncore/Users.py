# https://front.arcopole.fr/orion_fed_105/orion/admin/tree/rightmanagement/groups/__children
from .Subjects import Subjects
from .User import User


class Users(Subjects):
    """
    Class allowing to get access to the defined users

    """

    def __init__(self):
        super().__init__('users')

    def _get_system_subject_id(self):
        return []

    def _create_subject_instance(self, subject_title, subject_id, profile_id):
        return User(subject_title, subject_id, profile_id)
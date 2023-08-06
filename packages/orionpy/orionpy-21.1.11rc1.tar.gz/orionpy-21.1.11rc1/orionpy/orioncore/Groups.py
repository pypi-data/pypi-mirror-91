# https://front.arcopole.fr/orion_fed_105/orion/admin/tree/rightmanagement/groups/__children
from .Subjects import Subjects
from .Group import Group


class Groups(Subjects):
    """
    Class allowing to get access to the defined groups

    """

    def __init__(self):
        super().__init__('groups')

    def _get_system_subject_id(self):
        return ['org', 'public']

    def _create_subject_instance(self, subject_title, subject_id, profile_id):
        return Group(subject_title, subject_id, profile_id)
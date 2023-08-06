# https://front.arcopole.fr/orion_fed_105/orion/admin/tree/rightmanagement/groups/__children
import abc

from .Elements import Elements
from .Subject import Subject


class Subjects(Elements):
    """
    Class allowing to get access to the defined groups

    """

    def __init__(self, subject_type):
        super().__init__()
        
        self.subject_type = subject_type
        self.title_key = 'title'
        self.name_key = 'name'


    @abc.abstractmethod
    def _get_system_subject_id(self):
        """Return list of subject id"""
        raise NotImplementedError('class must define _get_system_subject_id() to use this base class')

    def _update(self):
        """Make sure that list of elements is up to date with DB state.
        Name is the key to get a particular group
        """
        subject_structs = self.request.get_in_python(self.url_manager.subject_list_url(self.subject_type))
        self._elements = {}
        for subject_struct in subject_structs:
            # Groups 'organisation' and 'tout le monde' require a specific treatment
            if subject_struct[self.name_key] in self._get_system_subject_id():
                subject_url = self.url_manager.subject_information_url(self.subject_type, subject_struct[self.name_key])
                subject_str = self.request.get_in_python(subject_url)
                profile_id = subject_str['properties']['builtinRole']
            else:
                profile_id = None
            
            subject_id = subject_struct[self.name_key]
            subject_title = subject_struct[self.title_key]

            self._elements[subject_title] = self._create_subject_instance(subject_title, subject_id, profile_id)

    @abc.abstractmethod
    def _create_subject_instance(self, subject_title, subject_id, profile_id):
        """Create instance of the specific subject"""
        raise NotImplementedError('class must define _create_subject_instance() to use this base class')

    def get_with_id(self, subject_id):
        """Look for a particular group in the list using its id

        :param group_id: id of the group to look for
        :return: the required group or None if nothing found
        """
        self._update()
        subject_id = subject_id.strip()
        for key, subject in self._elements.items():
            if subject.id == subject_id:
                return subject
        return None

    def all(self):
        """
        :return: the list of elements' values
        """
        # TODO convert to list ?
        self._update()
        return sorted(self._elements.values(),
                      key = lambda group: group.title.lower())

# stdlib
from typing import List, Optional
# libs
from cloudcix_rest.controllers import ControllerBase
# local
from contact.models import Exclusion


__all__ = [
    'ExclusionListController',
    'ExclusionCreateController',
    'ExclusionUpdateController',
]


class ExclusionListController(ControllerBase):
    """
    Validates User data used to list Exclusion records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific
        for this Controller
        """
        allowed_ordering = (
            'name',
            'id',
        )
        search_fields = {
            'name': ControllerBase.DEFAULT_STRING_FILTER_OPERATORS,
            'id': ControllerBase.DEFAULT_NUMBER_FILTER_OPERATORS,
        }


class ExclusionCreateController(ControllerBase):
    """
    Validates user data used to create Exclusion records
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Exclusion
        validation_order = (
            'classes',
            'name',
            'tags',
        )

    def validate_classes(self, classes: Optional[List[str]]) -> Optional[str]:
        """
        description: The array of classes to be excluded in HTML Documents
        type: array
        items:
            description: The name of a class to be excluded
            type: string
        """
        classes = classes or []
        if not isinstance(classes, list):
            return 'contact_exclusion_create_101'

        class_list: List[str] = []
        if len(classes):
            for class_name in classes:
                class_name = str(class_name).strip()
                if len(class_name) == 0:
                    return 'contact_exclusion_create_102'
                class_list.append(class_name)

        self.cleaned_data['classes'] = class_list
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Exclusion
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_exclusion_create_103'
        if len(name) > self.get_field('name').max_length:
            return 'contact_exclusion_create_104'
        if Exclusion.objects.filter(name=name, member_id=self.request.user.member['id']).exists():
            return 'contact_exclusion_create_105'
        self.cleaned_data['name'] = name
        return None

    def validate_tags(self, tags: Optional[List[str]]) -> Optional[str]:
        """
        description: The array of tags to be excluded in HTML Documents
        type: array
        items:
            description: The name of a tag to be excluded
            type: string
        """
        tags = tags or []
        if not isinstance(tags, list):
            return 'contact_exclusion_create_106'
        tag_list: List[str] = []
        if len(tags):
            for tag_name in tags:
                tag_name = str(tag_name).strip()
                if len(tag_name) == 0:
                    return 'contact_exclusion_create_107'
                tag_list.append(tag_name)

        self.cleaned_data['tags'] = tag_list
        return None


class ExclusionUpdateController(ControllerBase):
    """
    Validates User data used to update a Exclusion
    """
    class Meta(ControllerBase.Meta):
        """
        Override some of the ControllerBase.Meta fields to make them more specific for this Controller
        """
        model = Exclusion
        validation_order = (
            'classes',
            'name',
            'tags',
        )

    def validate_classes(self, classes: Optional[List[str]]) -> Optional[str]:
        """
        description: The array of classes to be excluded in HTML Documents
        type: array
        items:
            description: The name of a class to be excluded
            type: string
        """

        classes = classes or []
        if not isinstance(classes, list):
            return 'contact_exclusion_update_101'
        class_list: List[str] = []
        if len(classes):
            for class_name in classes:
                class_name = str(class_name).strip()
                if len(class_name) == 0:
                    return 'contact_exclusion_update_102'
                class_list.append(class_name)

        self.cleaned_data['classes'] = class_list
        return None

    def validate_name(self, name: Optional[str]) -> Optional[str]:
        """
        description: The name of the Exclusion
        type: string
        """
        if name is None:
            name = ''
        name = str(name).strip()
        if len(name) == 0:
            return 'contact_exclusion_update_103'
        if len(name) > self.get_field('name').max_length:
            return 'contact_exclusion_update_104'
        if Exclusion.objects.filter(
                name=name,
                member_id=self.request.user.member['id'],
        ).exclude(pk=self._instance.pk).exists():
            return 'contact_exclusion_update_105'
        self.cleaned_data['name'] = name
        return None

    def validate_tags(self, tags: Optional[List[str]]) -> Optional[str]:
        """
        description: The array of tags to be excluded in HTML Documents
        type: array
        items:
            description: The name of a tag to be excluded
            type: string
        """
        tags = tags or []
        if not isinstance(tags, list):
            return 'contact_exclusion_update_106'
        tag_list: List[str] = []
        if len(tags):
            for tag_name in tags:
                tag_name = str(tag_name).strip()
                if len(tag_name) == 0:
                    return 'contact_exclusion_update_107'
                tag_list.append(tag_name)

        self.cleaned_data['tags'] = tag_list
        return None

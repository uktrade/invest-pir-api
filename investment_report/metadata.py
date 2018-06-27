from rest_framework.metadata import SimpleMetadata
from rest_framework import serializers


class RelatedFieldMetadata(SimpleMetadata):
    def get_field_info(self, field):
        """
        Provides slug related field with allowed options
        """
        field_info = super().get_field_info(field)

        if isinstance(field, serializers.SlugRelatedField):
            if field.field_name == 'country':
                field_info['choices'] = [
                    {
                        'value': name,
                        'display_name': display_name
                    }
                    for name, display_name in
                    field.queryset.values_list('iso', 'name')
                ]

            if field.field_name == 'market':
                field_info['choices'] = [
                    {
                        'value': name,
                        'display_name': name
                    }
                    for name in
                    field.queryset.values_list('name', flat=True)
                ]

            if field.field_name == 'sector':
                field_info['choices'] = [
                    {
                        'value': name,
                        'display_name': display_name
                    }
                    for name, display_name in
                    field.queryset.values_list('name', 'display_name')
                ]

        return field_info

    def determine_actions(self, request, view):
        """
        Sig auth interferes with this. Had to remove the permission check
        that's in the superclass. Not a security issue as the view
        is behind sigauth anyway. Not sure why this happens.
        """
        serializer = view.get_serializer()
        return {'POST': self.get_serializer_info(serializer)}

from rest_framework import serializers


class CustomField(serializers.Field):
    def to_internal_value(self, data):
        return data

    def to_representation(self, value):
        return value


class ModelDocument(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.Meta.model._meta.fields:
            if field.name in self.fields:
                self.fields[field.name].help_text = field.get_internal_type()
                if field.get_internal_type() == "ForeignKey":
                    self.fields[field.name].help_text += f" -> {field.related_model.__name__}"

        for related in self.Meta.model._meta.related_objects:
            if related.one_to_many is True:
                self.fields[related.get_accessor_name()].help_text = f"Relation -> {related.related_model.__name__}"
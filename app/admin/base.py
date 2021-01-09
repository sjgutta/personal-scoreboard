from flask_admin.contrib.peewee import ModelView
from wtfpeewee.fields import SelectChoicesField

from app.models.fields import EnumField
from flask_admin.contrib.peewee.form import CustomModelConverter


class EnumSelectChoicesField(SelectChoicesField):

    def __init__(self, enum, **kwargs):
        kwargs.setdefault('choices', [(x, x.value) for x in enum])
        super(EnumSelectChoicesField, self).__init__(**kwargs)
        self.enum = enum
        self.coerce = self._coerce_enum

        if self.allow_blank:
            self.validators = []

    def iter_choices(self):
        if self.allow_blank:
            yield (u'__None', self.blank_text, self.data is None)

        for value, label in self.choices:
            # Using `value.name` instead of just `value`
            yield (value.name, label, self.coerce(value) == self.data)

    def _coerce_enum(self, value):
        if isinstance(value, self.enum):
            return value
        elif value is None and self.allow_blank:
            return value
        else:
            return self.enum[value]

    def pre_validate(self, form):
        if self.coerce(self.data) in [x[0] for x in self.choices]:
            return
        else:
            super(EnumSelectChoicesField, self).pre_validate(form)


class ModelConverter(CustomModelConverter):
    def __init__(self, view, additional=None):
        super().__init__(view, additional)
        self.converters[EnumField] = self.enum_converter

    def enum_converter(self, model, field, **kwargs):
        choices = field.choices
        allow_blank = kwargs.pop('allow_blank', field.null)
        kwargs.update({
            'choices': choices,
            'allow_blank': allow_blank})

        return field.name, EnumSelectChoicesField(field.enum, **kwargs)


# preparing this for later if admin expands
class BaseModelView(ModelView):
    can_delete = False
    model_form_converter = ModelConverter


from django.db import models
from django import forms
from django.utils import simplejson as json


class JSONWidget(forms.Textarea):

    def render(self, name, value, attrs=None):
        if isinstance(value, dict):
            value = json.dumps(value, indent=2)
        return super(JSONWidget, self).render(name, value, attrs)


class JSONFormField(forms.CharField):

    def __init__(self, *args, **kwargs):
        kwargs['widget'] = JSONWidget
        super(JSONFormField, self).__init__(*args, **kwargs)

    def clean(self, value):
        if not value:
            return None
        try:
            return json.loads(value)
        except Exception, exception:
            raise forms.ValidationError(u'JSON decode error: %s' % (unicode(exception),))


class JSONField(models.TextField):
    __metaclass__ = models.SubfieldBase

    def formfield(self, **kwargs):
        return super(JSONField, self).formfield(form_class=JSONFormField, **kwargs)

    def to_python(self, value):
        if not value:
            return None
        try:
            if isinstance(value, basestring):
                return json.loads(value)
        except ValueError:
            pass
        return value

    def get_db_prep_save(self, value, *args, **kwargs):
        if not value:
            return None
        if isinstance(value, dict):
            value = json.dumps(value)
        return super(JSONField, self).get_db_prep_save(value, *args, **kwargs)

    def value_to_string(self, obj):
        value = self._get_val_from_obj(obj)
        return self.get_db_prep_value(value)


try:
    from south.modelsinspector import add_introspection_rules
    add_introspection_rules([], ['^fiber\.utils\.json\.JSONField'])
except ImportError:
    pass
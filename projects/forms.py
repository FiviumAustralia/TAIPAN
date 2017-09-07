from django.forms import Form, TextInput, Textarea
from django.forms.models import modelform_factory
from .models import BuildDetail


class ModelFormWidgetMixin(object):
    def get_form_class(self):
        return modelform_factory(self.model, fields=self.fields, widgets=self.widgets)


class BuildForm(Form):
    fields = ['name', 'description']
    widgets = {
        'name': TextInput(attrs={'class': 'small-field'}),
        'description': Textarea(attrs={'class': 'large-field'}),
    }

    class Meta:
        model = BuildDetail
from django import forms

from .models import Resource, Volunteer


class VolunteerForm(forms.ModelForm):
    class Meta:
        model = Volunteer
        fields = ('real_name', 'email_address', 'phone_number')
        labels = {'real_name': 'Full Name'}

    def __init__(self, *args, **kwargs):
        resources = kwargs.pop('resources')
        super().__init__(*args, **kwargs)

        for resource in resources:
            if resource.visible:
                resource_type = Resource.Type(resource.type)
                if resource_type == Resource.Type.boolean:
                    field = forms.BooleanField(required=False)
                else:
                    attrs = {
                        'min': resource.min_value,
                        'target': resource.target_value
                    }

                    if resource.target_value - resource.min_value <= 20:
                        attrs['type'] = 'range'

                    widget = forms.NumberInput(attrs=attrs)

                    field = forms.IntegerField(min_value=resource.min_value,
                                               target_value=resource.target_value,
                                               widget=widget,
                                               initial=str(resource.default_value))

            else:
                # field = forms.
                field.widget = forms.HiddenInput()
                field.value = resource.default_value

            field.label = resource.name

            self.fields[self.get_id_for_resource(resource)] = field

        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'

    def get_id_for_resource(self, resource):
        return 'q{}'.format(resource.id)

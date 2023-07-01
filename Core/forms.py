from django import forms

from Core.models import Plant


class AddPlantForm(forms.ModelForm):
    class Meta:
        model = Plant
        fields = ['name', 'photo', 'ec', 'ph', 'npk', 'temperature', 'ideal_moisture', 'fertilizer']

    def clean(self):
        clean_data = super().clean()
        name = clean_data.get("name")


    # def __init__(self, *args, **kwargs):
    #     super(AddPlantForm, self).__init__(*args, **kwargs)
    #     for field in self.fields:
    #         self.fields[field].widget.attrs['class'] = 'form-field'
    #         self.fields[field].widget.attrs['placeholder'] = f'Enter {field}'


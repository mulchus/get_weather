from django import forms

class CityForm(forms.Form):
    city = forms.CharField(
        label='Введите название города',
        max_length=100,
    )

    def __init__(self, *args, **kwargs):
        super(CityForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'

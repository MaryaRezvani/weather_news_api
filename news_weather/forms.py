from django import forms
from .regions import regions

class CityForm(forms.Form):

    STATE_CHOICES = [(state, state) for state in regions.keys()]
    state = forms.ChoiceField(
        choices=STATE_CHOICES,
        label="انتخاب استان",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'state-select'})
    )
    city = forms.ChoiceField(
        choices=[],
        label="انتخاب شهر",
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'city-select'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'state' in self.data:
            state = self.data['state']
            self.fields['city'].choices = [(city, city) for city in regions.get(state, [])]
        else:
            self.fields['city'].choices = []
        if not self.data.get('state') and self.STATE_CHOICES:
            default_state = self.STATE_CHOICES[0][0]
            self.fields['state'].initial = default_state
            self.fields['city'].choices = [(city, city) for city in regions.get(default_state, [])]
            self.fields['city'].initial = self.fields['city'].choices[0][0]

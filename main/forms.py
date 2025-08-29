from django import forms
from .models import Tifo

class TifoForm(forms.ModelForm):
    class Meta:
        model = Tifo
        fields = ['date', 'tifo_type', 'match', 'description', 'picture'] 
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={'type': 'date', 'placeholder': 'Select a date'}
            )
        }

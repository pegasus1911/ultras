from django import forms
from .models import Tifo
from django.core.files.uploadedfile import UploadedFile

class TifoForm(forms.ModelForm):
    class Meta:
        model = Tifo
        fields = ['date', 'tifo_type', 'match', 'description', 'picture']
        widgets = {
            'date': forms.DateInput(
                format='%Y-%m-%d',
                attrs={
                    'type': 'date',
                    'placeholder': 'Select a date',
                    'class': 'date-input'
                }
            ),
            'description': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Describe the tifo'}),
            'match': forms.TextInput(attrs={'placeholder': 'Match name or teams'}),
        }

    # Optional: clear picture if user wants to remove it when editing
    
def clean_picture(self):
    picture = self.cleaned_data.get('picture')
    # Only check size if it's a newly uploaded file
    if picture and isinstance(picture, UploadedFile):
        if picture.size > 5 * 1024 * 1024:  # 5MB limit
            raise forms.ValidationError("Image file too large ( > 5MB ).")
    return picture

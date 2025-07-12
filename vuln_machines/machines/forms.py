from django import forms
from .models import VulnerableMachine

class VulnerableMachineForm(forms.ModelForm):
    class Meta:
        model = VulnerableMachine
        fields = '__all__'
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
            'writeups': forms.Textarea(attrs={'rows': 3}),
            'cases_list': forms.Textarea(attrs={'rows': 3}),
            'additional_versions': forms.Textarea(attrs={'rows': 3}),
            'tags': forms.TextInput(attrs={'placeholder': 'RCE, SQLi, XSS'}),
            'detected_in': forms.CheckboxSelectMultiple(choices=VulnerableMachine.SECURITY_SYSTEMS),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['wiki_link'].required = False
        self.fields['writeups'].required = False
        self.fields['cases_list'].required = False
        self.fields['additional_versions'].required = False
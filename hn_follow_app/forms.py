from django import forms

class AddHnUserForm(forms.Form):
    username = forms.CharField(label='HN Username', max_length=100)
    notes = forms.CharField(label='Notes', widget=forms.Textarea, required=False)
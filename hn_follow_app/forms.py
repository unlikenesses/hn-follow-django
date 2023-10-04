from django import forms


class AddHnUserForm(forms.Form):
    username = forms.CharField(
        label=False,
        max_length=100,
        widget=forms.TextInput(attrs={"placeholder": "Username"}),
    )
    notes = forms.CharField(
        label=False,
        widget=forms.Textarea(attrs={"placeholder": "Notes"}),
        required=False,
    )

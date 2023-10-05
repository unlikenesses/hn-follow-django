from django import forms
from .models import HnUser


class HnUserForm(forms.ModelForm):
    class Meta:
        model = HnUser
        fields = ["username", "notes"]
        labels = {
            "username": "",
            "notes": "",
        }
        widgets = {
            "username": forms.TextInput(
                attrs={
                    "placeholder": "Username",
                    "class": "mb-4 rounded-md shadow-sm border-gray-900 focus:border-orange-300 focus:ring focus:ring-orange-200 focus:ring-opacity-50",
                }
            ),
            "notes": forms.Textarea(
                attrs={
                    "placeholder": "Notes",
                    "class": "mb-4 rounded-md shadow-sm border-gray-900 focus:border-orange-300 focus:ring focus:ring-orange-200 focus:ring-opacity-50",
                }
            ),
        }

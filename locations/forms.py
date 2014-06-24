from django import forms
from django.utils.timezone import now


class Location(forms.Form):

    location = forms.CharField()
    email = forms.EmailField()

    @property
    def data_as_email(self):
        return {
            "subject": self.cleaned_data["location"],
            "address": self.cleaned_data["email"],
            "date": now()
        }
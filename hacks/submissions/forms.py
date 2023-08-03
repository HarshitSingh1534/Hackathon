from django import forms
from django.utils import timezone
from .models import Hackathon, Submission
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class HackathonForm(forms.ModelForm):
    class Meta:
        model = Hackathon
        fields = ['title', 'description', 'background_image', 'hackathon_image',
                  'type_of_submission', 'start_datetime', 'end_datetime', 'reward_prize']

    def clean(self):
        cleaned_data = super().clean()
        start_datetime = cleaned_data.get('start_datetime')
        end_datetime = cleaned_data.get('end_datetime')

        if start_datetime and end_datetime:
            if start_datetime >= end_datetime:
                raise forms.ValidationError("The start datetime must be earlier than the end datetime.")

            current_time = timezone.now()
            if start_datetime < current_time or end_datetime < current_time:
                raise forms.ValidationError("The start and end datetime cannot be in the past.")

        return cleaned_data



class SubmissionForm(forms.ModelForm):
    class Meta:
        model = Submission
        fields = ['submission_name', 'summary', 'image_submission', 'file_submission', 'link_submission']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        hackathon = kwargs.get('instance', None)
        if hackathon:
            allowed_submission_type = hackathon.type_of_submission
            if allowed_submission_type == 'image':
                self.fields['file_submission'].widget = forms.HiddenInput()
                self.fields['link_submission'].widget = forms.HiddenInput()
            elif allowed_submission_type == 'file':
                self.fields['image_submission'].widget = forms.HiddenInput()
                self.fields['link_submission'].widget = forms.HiddenInput()
            elif allowed_submission_type == 'link':
                self.fields['image_submission'].widget = forms.HiddenInput()
                self.fields['file_submission'].widget = forms.HiddenInput()

    def clean(self):
        cleaned_data = super().clean()
        image_submission = cleaned_data.get('image_submission')
        file_submission = cleaned_data.get('file_submission')
        link_submission = cleaned_data.get('link_submission')

        if image_submission and (file_submission or link_submission):
            raise forms.ValidationError("Only one submission type is allowed.")

        if file_submission and (image_submission or link_submission):
            raise forms.ValidationError("Only one submission type is allowed.")

        if link_submission and (image_submission or file_submission):
            raise forms.ValidationError("Only one submission type is allowed.")

        return cleaned_data
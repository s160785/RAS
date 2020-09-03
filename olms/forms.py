from django import forms
from .models import UserProfile, Leaves
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput, TimePickerInput
import re


class newLeave(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = ('reason', 'description', 'proof', 'out_date', 'in_date')
        widgets = {
            'out_date': DateTimePickerInput,
            'in_date': DateTimePickerInput,
        }


class student(UserCreationForm):
    id = forms.CharField(max_length=7, label='Id', widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    branch = forms.ChoiceField(
        choices=UserProfile.branches, label='Branch')
    year = forms.ChoiceField(choices=UserProfile.years, label='Year',
                             widget=forms.Select(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['id', 'username', 'password1', 'password2']

    def clean(self):
        cd = super().clean()
        if UserProfile.objects.filter(id=cd.get('id').capitalize()).first() is not None:
            raise forms.ValidationError(
                'Account with this Id no. already exists\nIf this Id no. belongs to you, report to the mail_id:rahulpinjarla@gmail.com')

        if not re.match(r'[s,S][0-9]{6}', cd.get('id')):
            raise forms.ValidationError('Invalid id no')

        if (cd.get('branch') == 'puc' and (cd.get('year') != ('p1' or 'p2'))) or (cd.get('branch') != 'puc' and (cd.get('year') == ('p1' or 'p2'))):
            raise forms.ValidationError('Invalid year and branch combination ')

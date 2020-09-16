from django import forms
from .models import UserProfile, Leaves, Personal_info
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.template.defaultfilters import filesizeformat
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
        labels = {
            'proof': "Allowed file types => 'pdf', 'doc', 'docx', 'jpg', 'png', 'xlsx', 'xls'"
        }

    def clean(self):
        cd = super().clean()
        if cd.get('out_date') > cd.get('in_date'):
            raise forms.ValidationError(
                'Out date should be lower than in date')
        if cd.get('proof'):
            if cd.get('proof').size > settings.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(('Please keep filesize under %s. Current filesize %s') % (
                    filesizeformat(settings.MAX_UPLOAD_SIZE), filesizeformat(cd.get('proof').size)))


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


class pform(forms.ModelForm):

    class Meta:
        model = Personal_info
        exclude = ('userprofile',)
        widgets = {
            'address': forms.Textarea()
        }

    def clean(self):
        cd = super().clean()
        if not re.match(r'^\d{12}$', str(cd.get('aadhar_no'))):
            raise forms.ValidationError('Invalid aadhar number')

        if not re.match(r'^\d{10}$', str(cd.get('phone_no'))) or not re.match(r'^\d{10}$', str(cd.get('parent_phn_no'))):
            raise forms.ValidationError('Invalid phone number')

        if not re.match(r'^[a-zA-Z, ]+$', str(cd.get('parent_name'))):
            raise forms.ValidationError('Invalid parent name')

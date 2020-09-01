from django import forms
from .models import UserProfile as user, Leaves
from bootstrap_datepicker_plus import DatePickerInput, DateTimePickerInput, TimePickerInput


class newLeave(forms.ModelForm):
    class Meta:
        model = Leaves
        fields = ('reason', 'description', 'proof', 'out_date', 'in_date')
        widgets = {
            'out_date': DateTimePickerInput,
            'in_date': DateTimePickerInput,
        }

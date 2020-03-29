
from django import forms
from django.forms import CharField, Form, PasswordInput
from datetime import datetime, date





class ContactForm(forms.Form):
    first_name = forms.CharField(required=False)
    last_name = forms.CharField()
    username = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': 'usualy personal number'}))
    password = forms.CharField(widget=PasswordInput(attrs = {'placeholder': 'Something Easy To Remember'}))
    category = forms.ChoiceField(choices=[('pilot', 'Pilot'), ('navigator', 'Navigator')])
    status = forms.ChoiceField(choices=[('Azach', 'Azach'), ('Miluim', 'Miluim')])
    movil = forms.ChoiceField(choices=[('1', 'Yes'), ('0', 'Not Yet')])


class LoginForm(forms.Form):
    username = forms.CharField(widget=forms.Textarea(attrs = {'placeholder': 'usualy personal number'}))
    password = forms.CharField()

class goalupdateForm(forms.Form):
    azach_num = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': 'Enter Here Azach Goal'}))
    miluim_num = forms.CharField(widget=forms.TextInput(attrs = {'placeholder': 'Enter Here Miluim Goal'}))

class ContactMe(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs = {'class': 'form-control', 'placeholder': 'Write A Letter/ Request To The Kahadit'}))


class AddShiftForm(forms.Form):
    flight_type = forms.ChoiceField(choices=[('30', '30'), ('7', '7'), ('Photo', 'Photo'), ('odem', 'Odem'), ('ogen', 'Ogen')])
    flight_date = forms.DateTimeField()
    notes = forms.CharField(required = False)

    def clean(self):
        cleaned_data = super(AddShiftForm, self).clean()
        flight_type = cleaned_data.get('flight_date')
        flight_date = cleaned_data.get('flight_date')
        notes = cleaned_data.get('notes')
        if not flight_type and not flight_date:
            raise forms.ValidationError('You have to write something!')








from django import forms

class NameForm(forms.Form):
    username = forms.CharField(label='Name', max_length=100)
    password = forms.CharField(widget=forms.PasswordInput(), label='Password', max_length=100)
    is_new_user = forms.BooleanField(label='New User?', required=False)
from django import forms
import getch.models as m
from allauth.account.forms import LoginForm

class CustomLoginForm(LoginForm):
    def __init__(self, *args, **kwargs):
        super(CustomLoginForm, self).__init__(*args, **kwargs)
        self.fields['login'].widget = forms.TextInput(attrs={
            'type': 'email',
            'placeholder': '이메일',
            'autofocus': 'autofocus',
            'class': 'form-control'
        })



class ResearchItemForm(forms.ModelForm):
    class Meta:
        model = m.ResearchItem
        fields = ('research','order','type','gender','preq','text',)
        # widgets = {
        #     'date_range': forms.Select(choices=DropdownModel.CHOICES)
        # }

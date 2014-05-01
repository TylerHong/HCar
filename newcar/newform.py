from django import forms

class BuyRequestForm(forms.Form):
    nickname = forms.CharField()
    cellphone = forms.CharField()
    email = forms.CharField()
    passwd = forms.CharField()

from django import forms

class Survey1Form(forms.Form):
    nickname = forms.CharField(widget=forms.TextInput)
    birth = forms.DateField(widget=forms.TextInput)
    pass

class Survey2Form(forms.Form):
    pass

class Survey3Form(forms.Form):
    pass
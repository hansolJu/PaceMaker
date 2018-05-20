from django import forms
from django.contrib.auth import get_user_model


class LoginForm(forms.ModelForm):
    hukbun = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '학번'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': '패스워드'}))

    class Meta:
        model = get_user_model()  # Student
        fields = ['hukbun', 'password']


class AgreeForm(forms.Form):
    agreeDataUsing = forms.BooleanField()

    agreeDataUsingValue = '쿠티스 정보 동의쿠티스 정보 동의쿠티스 정보 동의쿠티스 ' \
                          '정보 동의쿠티스 정보 동의쿠티스 정보 동의쿠티스 정보 동의 \n 쿠티스 정보 동의쿠티스 정보 ' \
                          '동의쿠티스 정보 동의쿠티스 정보 동의쿠티스 정보 동의쿠티스 정보 동의'
    fields = ['agreeDataUsing']

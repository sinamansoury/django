from django import forms
from django.core.exceptions import ValidationError


class AccountRegisterForm(forms.Form):
    username = forms.CharField(
        label='نام کاربری',
        widget=forms.TextInput()
    )
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        label='رمزعبور',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='تایید رمز عبور',
        widget=forms.PasswordInput()
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('رمز عبور با  تایید رمز عبور مغایرت دارد')


class AccountLoginForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput()
    )
    password = forms.CharField(
        label='رمزعبور',
        widget=forms.PasswordInput()
    )


class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput()
    )


class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='رمزعبور',
        widget=forms.PasswordInput()
    )
    confirm_password = forms.CharField(
        label='تایید رمز عبور',
        widget=forms.PasswordInput()
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('رمز عبور با  تایید رمز عبور مغایرت دارد')
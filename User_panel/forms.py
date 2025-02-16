from django import forms
from django.core.exceptions import ValidationError
from Account.models import User, AuthUser


class EditInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'id_code', 'email', 'birthday', 'avatar', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                     'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                    'class': 'form-control'
            }),
            'id_code': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'birthday': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control'
            }),

            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,

            }),
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'address': 'آدرس',
        }


class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label='رمزعبور فعلی',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    password = forms.CharField(
        label='رمزعبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )
    confirm_password = forms.CharField(
        label='تایید رمز عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control'
        })
    )

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password == confirm_password:
            return confirm_password
        raise ValidationError('رمز عبور با  تایید رمز عبور مغایرت دارد')


class AuthenticatedForm(forms.ModelForm):
    class Meta:
        model = AuthUser
        fields = ['pic', 'back_pic', 'front_pic', 'address_auth', 'address_auth_pic']
        widgets = {
            'front_pic': forms.FileInput(attrs={
                     'class': 'form-control',
            }),
            'back_pic': forms.FileInput(attrs={
                    'class': 'form-control'
            }),
            'pic': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address_auth': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 1,
                'placeholder': ' کد پستی',


            }),
            'address_auth_pic': forms.FileInput(attrs={
                'class': 'form-control',

            }),
        }

    def clean_address_auth(self):
        address_auth = self.cleaned_data.get('address_auth')
        if address_auth is None or address_auth < 1000000000 or address_auth > 9999999999:
            raise forms.ValidationError(" کد پستی باید دقیقاً ۱۰ رقم باشد.")
        return address_auth


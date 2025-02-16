from django import forms
from django.forms import ModelForm
from ContactUs.models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['fullname', 'email', 'title', 'message']
        widgets = {
            'fullname': forms.TextInput(attrs={
                'placeholder': 'نام و نام خانوادگی',
                'class': 'form-control'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'عنوان',
                'class': 'form-control',
            }),
            'title': forms.TextInput(attrs={
                'placeholder': 'عنوان',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'پیام شما',
                'class': 'form-control',
                'id': 'message'
            })
        }
        error_messages = {
            'fullname': {
                'required': 'لطفا نام و نام خانوادکی خود را بنویسید'
            },
            'message': {
                'required': 'لطفا پیام خود را بنویسید'
            },
            'title': {
                'required': 'لطفا عنوان خود را بنویسید'
            },
            'email': {
                'required': 'لطفا ایمیل خود را بنویسید'
            }
        }



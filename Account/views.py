from django.http import Http404, HttpResponse, HttpRequest
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import View
from Account.forms import AccountRegisterForm, AccountLoginForm, ForgotPasswordForm, ResetPasswordForm
from tracking.mixins import LoggingMixins
from .models import User
from django.utils.crypto import get_random_string
from django.contrib.auth import login, logout
from utils.email_service import send_email
# Create your views here.


class AccountSignupView(LoggingMixins, View):
    def get(self, request):
        register_form = AccountRegisterForm()
        return render(request, 'Account/signup.html', {
            'register_form': register_form
        })

    def post(self, request):
        register_form = AccountRegisterForm(request.POST)
        if register_form.is_valid():
            email = register_form.cleaned_data.get('email')
            name = register_form.cleaned_data.get('username')
            password = register_form.cleaned_data.get('password')
            user_email_check = User.objects.filter(email=email).exists()
            user_name_check = User.objects.filter(username=name).exists()
            if user_email_check and user_name_check:
                register_form.add_error('username', 'نام کاربری وارد شده قبلا استفاده شده است')
                register_form.add_error('email', 'ایمیل وارد شده قبلا استفاده شده است')
            elif user_name_check:
                register_form.add_error('username', 'نام کاربری وارد شده قبلا استفاده شده است')
            elif user_email_check:
                register_form.add_error('email', 'ایمیل وارد شده قبلا استفاده شده است')
            else:
                new_user = User(email=email,
                                username=name,
                                email_verified=get_random_string(48),
                                is_active=False)
                new_user.set_password(password)
                new_user.save()
                send_email('فعالسازی حساب کاربری', new_user.email, {'user': new_user},
                           'email/account_activation_email.html')
                return redirect(reverse('Login'))

        return render(request, 'Account/signup.html', {
            'register_form': register_form
        })


class AccountLoginView(LoggingMixins, View):
    def get(self, request):
        login_form = AccountLoginForm()
        return render(request, 'Account/login.html', {
            'login_form': login_form
        })

    def post(self, request: HttpRequest):
        login_form = AccountLoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user: User = User.objects.filter(email=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'کاربر پیدا نشد')
                else:
                    is_pass_correct = user.check_password(user_pass)
                    if is_pass_correct:
                        login(request, user)
                        return redirect(reverse('index'))
                    else:
                        login_form.add_error('password', 'رمز اشتباه است')
            else:

                login_form.add_error('email', 'کاربر پیدا نشد')
            return render(request, 'Account/login.html', {
                'login_form': login_form
            })


class ActivatedCodeView(LoggingMixins, View):
    def get(self, request, email_verified):
        user: User = User.objects.filter(email_verified=email_verified).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_verified = get_random_string(48)
                user.save()
                return redirect(reverse('Login'))
            else:
                pass
        raise Http404


class ForgotPasswordView(LoggingMixins, View):
    def get(self, request):
        forget_form = ForgotPasswordForm()
        return render(request, 'Account/forget.html', {
            'forget_form': forget_form
        })

    def post(self, request):
        forget_form = ForgotPasswordForm(request.POST)
        if forget_form.is_valid():
            user_email = forget_form.cleaned_data.get('email')
            user: User = User.objects.filter(email=user_email).first()
            if user is not None:
                pass
            else:
                forget_form.add_error('email', 'کاربر وجود ندارد')
        return render(request, 'Account/forget.html', {
            'forget_form': forget_form
        })


class ResetPasswordView(LoggingMixins, View):
    def get(self, request, email_verified):
        user: User = User.objects.filter(email_verified=email_verified).first()
        if user is None:
            return redirect(reverse('Login'))
        reset_form = ResetPasswordForm()
        return render(request, 'Account/reset.html', {
            'reset_form': reset_form,
            'user': user
            })

    def post(self, request, email_verified):
        reset_form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_verified=email_verified).first()
        if reset_form.is_valid():
            if user is None:
                return redirect(reverse('Login'))
            new_password = reset_form.cleaned_data.get('password')
            user.set_password(new_password)
            user.email_verified = get_random_string(48)
            user.is_active = True
            user.save()
            return redirect(reverse('Login'))
        return render(request, 'Account/reset.html', {
            'reset_form': reset_form,
            'user': user
        })


class LogoutView(LoggingMixins, View):
    def get(self, request):
        logout(request)
        return redirect(reverse('index'))

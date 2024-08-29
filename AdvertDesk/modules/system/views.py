from django.contrib import messages
from django.contrib.auth import get_user_model, login
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.sites.models import Site
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.utils import timezone
from django.views import View
from django.views.generic import DetailView, UpdateView, CreateView, TemplateView, FormView
from django.contrib.auth.views import (LoginView, LogoutView,
                                       PasswordChangeView, PasswordResetView, PasswordResetConfirmView,
                                       )
from django.db import transaction
from django.urls import reverse_lazy

from .models import Profile
from .forms import (UserUpdateForm, ProfileUpdateForm, UserRegisterForm,
                    UserLoginForm, UserPasswordChangeForm, UserForgotPasswordForm, UserSetNewPasswordForm,
                    OTPConfirmationForm,
                    )
from AdvertDesk import settings
from ..services.mixins import UserIsNotAuthenticated
from ..services.utils import generate_otp

User = get_user_model()


class ProfileDetailView(DetailView):
    """
    Представление для просмотра профиля
    """
    model = Profile
    context_object_name = 'profile'
    template_name = 'system/profile_detail.html'
    # способ не создавая менеджер модели, оптимизировать SQL во views.py
    queryset = model.objects.all().select_related('user')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Страница пользователя: {self.object.user.username}'
        return context


class ProfileUpdateView(UpdateView):
    """
    Представление для редактирования профиля
    """
    model = Profile
    form_class = ProfileUpdateForm
    template_name = 'system/profile_edit.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = f'Редактирование профиля пользователя: {self.request.user.username}'
        if self.request.POST:
            context['user_form'] = UserUpdateForm(self.request.POST, instance=self.request.user)
        else:
            context['user_form'] = UserUpdateForm(instance=self.request.user)
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        user_form = context['user_form']
        with transaction.atomic():
            if all([form.is_valid(), user_form.is_valid()]):
                user_form.save()
                form.save()
            else:
                context.update({'user_form': user_form})
                return self.render_to_response(context)
        return super(ProfileUpdateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.object.slug})


class UserLoginView(SuccessMessageMixin, LoginView):
    """
    Авторизация на сайте
    """
    form_class = UserLoginForm
    template_name = 'system/registration/user_login.html'
    next_page = 'adverts_home'
    success_message = 'Добро пожаловать на сайт!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Авторизация на сайте'
        return context


class UserLogoutView(LogoutView):
    """
    Выход с сайта
    """
    next_page = reverse_lazy('adverts_home')


class UserPasswordChangeView(SuccessMessageMixin, PasswordChangeView):
    """
    Изменение пароля пользователя
    """
    form_class = UserPasswordChangeForm
    template_name = 'system/registration/user_password_change.html'
    success_message = 'Ваш пароль был успешно изменён!'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Изменение пароля на сайте'
        return context

    def get_success_url(self):
        return reverse_lazy('profile_detail', kwargs={'slug': self.request.user.profile.slug})


class UserForgotPasswordView(SuccessMessageMixin, PasswordResetView):
    """
    Представление по сбросу пароля по почте
    """
    form_class = UserForgotPasswordForm
    template_name = 'system/registration/user_password_reset.html'
    success_url = reverse_lazy('adverts_home')
    success_message = 'Письмо с инструкцией по восстановлению пароля отправлено на ваш email'
    subject_template_name = 'system/email/password_subject_reset_mail.txt'
    email_template_name = 'system/email/password_reset_mail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Запрос на восстановление пароля'
        return context


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """
    Представление установки нового пароля
    """
    form_class = UserSetNewPasswordForm
    template_name = 'system/registration/user_password_set_new.html'
    success_url = reverse_lazy('adverts_home')
    success_message = 'Пароль успешно изменен. Можете авторизоваться на сайте.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Установить новый пароль'
        return context


class UserRegisterView(UserIsNotAuthenticated, CreateView):
    """
    Представление регистрации на сайте с формой регистрации
    """
    form_class = UserRegisterForm
    success_url = reverse_lazy('email_confirmation_sent')
    template_name = 'system/registration/user_register.html'
    success_message = 'Код подтверждения отправлен на вашу почту.'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Регистрация на сайте'
        return context

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.save()

        profile = Profile.objects.get(user=user)
        profile.email_confirmed = False
        otp = generate_otp()
        profile.otp = otp
        profile.otp_created_at = timezone.now()
        profile.save()

        current_site = Site.objects.get_current().domain
        send_mail(
            'Подтвердите свой электронный адрес',
            f'Ваш код: {otp}. Пожалуйста, введите его на странице подтверждения: '
            f'http://{current_site}{reverse_lazy("verify_email")}',
            [settings.DEFAULT_FROM_EMAIL],
            [user.email],
            fail_silently=False,
        )
        login(self.request, user)
        return redirect('email_confirmation_sent')


class OTPVerificationView(FormView):
    """
    Подтверждение почты через ОТР
    """
    form_class = OTPConfirmationForm
    template_name = 'system/registration/verify_otp.html'
    success_url = reverse_lazy('email_confirmed')

    def form_valid(self, form):
        otp = form.cleaned_data['otp']
        try:
            profile = self.request.user.profile
            if profile.otp == otp and profile.is_otp_valid():
                profile.email_confirmed = True
                profile.otp = None
                profile.otp_created_at = None
                profile.save()
                # messages.success(self.request, 'Email успешно подтвержден.')
                return super().form_valid(form)
            else:
                form.add_error('otp', 'Неверный OTP или OTP истек.')
        except Profile.DoesNotExist:
            form.add_error('otp', 'Профиль пользователя не найден.')
        return self.form_invalid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Подтверждение email'
        context['can_request_new_otp'] = self.request.user.is_authenticated and not self.request.user.profile.email_confirmed
        return context


class RequestNewOTPView(View):
    def get(self, request):
        user = request.user
        if user.is_authenticated and not user.profile.email_confirmed:
            profile = user.profile
            otp = generate_otp()
            profile.otp = otp
            profile.otp_created_at = timezone.now()
            profile.save()

            current_site = Site.objects.get_current().domain
            send_mail(
                'Новый код подтверждения',
                f'Ваш новый код: {otp}. Пожалуйста, введите его на странице подтверждения: '
                f'http://{current_site}{reverse_lazy("verify_email")}',
                [settings.DEFAULT_FROM_EMAIL],
                [user.email],
                fail_silently=False,
            )
            messages.success(request, 'Новый код подтверждения отправлен на вашу почту.')
        else:
            messages.error(request, 'Вы не можете запросить новый код.')
        return redirect('verify_email')


class EmailConfirmationSentView(TemplateView):
    template_name = 'system/registration/email_confirmation_sent.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Письмо активации отправлено'
        return context


class EmailConfirmedView(TemplateView):
    template_name = 'system/registration/email_confirmed.html'
    success_url = reverse_lazy('adverts_home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес активирован'
        return context


class EmailConfirmationFailedView(TemplateView):
    template_name = 'system/registration/email_confirmation_failed.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Ваш электронный адрес не активирован'
        return context

# Create your views here.

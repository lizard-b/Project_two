from django.contrib.auth.mixins import AccessMixin
from django.contrib import messages
from django.shortcuts import redirect


class AuthorRequiredMixin(AccessMixin):

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()
        if request.user.is_authenticated:
            if request.user.username != self.get_object().author or request.user.is_staff:
                messages.info(request, 'Изменение и удаление статьи доступно только автору')
                return redirect('adverts_home')
        return super().dispatch(request, *args, **kwargs)

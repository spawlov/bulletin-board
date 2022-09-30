from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied


class AdvertOwnerRequiredMixin(LoginRequiredMixin):
    """Дополнительная проверка на владельца объявления"""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return self.handle_no_permission()

        elif self.get_object().author.id != self.request.user.id:
            raise PermissionDenied()

        return super().dispatch(request, *args, **kwargs)

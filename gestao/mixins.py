from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin, UserPassesTestMixin):
    role_required = None

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.role == self.role_required

    def handle_no_permission(self):
        if self.request.user.is_authenticated:
            raise PermissionDenied
        return super().handle_no_permission()


class RequerenteRequiredMixin(RoleRequiredMixin):
    role_required = "requerente"


class ResponsavelRequiredMixin(RoleRequiredMixin):
    role_required = "responsavel"


class AdminRequiredMixin(RoleRequiredMixin):
    role_required = "admin"
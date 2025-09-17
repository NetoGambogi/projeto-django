from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy

class CustomLoginView(LoginView):
    template_name = "auth/login.html"

    def get_success_url(self):
        user = self.request.user

        if user.role == "admin":
            return reverse_lazy("admin_dashboard")
        
        elif user.role == "responsavel":
            return reverse_lazy("responsavel_dashboard")
        return reverse_lazy("chamado_list")
    
class CustomLogoutView(LogoutView):
    next_page = reverse_lazy("login")
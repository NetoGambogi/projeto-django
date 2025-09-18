import django_filters
from gestao.models import Chamado, CustomUser

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    email = django_filters.CharFilter(lookup_expr='icontains')
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email']
        
class ChamadoFilter(django_filters.FilterSet):
    titulo = django_filters.CharFilter(field_name="titulo", lookup_expr='icontains')
    status = django_filters.ChoiceFilter(field_name="status", choices=Chamado.STATUS_CHOICES,)
    
    class Meta:
        model = Chamado
        fields = ['titulo', 'status']
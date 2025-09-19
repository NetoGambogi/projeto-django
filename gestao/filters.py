import django_filters
from gestao.models import Chamado, CustomUser

class UserFilter(django_filters.FilterSet):
    username = django_filters.CharFilter(lookup_expr='icontains')
    role = django_filters.ChoiceFilter(choices=CustomUser.ROLE_CHOICES)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'role']
        
class ChamadoFilter(django_filters.FilterSet):
    id = django_filters.CharFilter(field_name="id")
    titulo = django_filters.CharFilter(field_name="titulo", lookup_expr='icontains')
    status = django_filters.ChoiceFilter(field_name="status", choices=Chamado.STATUS_CHOICES,)
    
    class Meta:
        model = Chamado
        fields = ['id','titulo', 'status']
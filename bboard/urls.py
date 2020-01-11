from django.urls import path

from .views import index, by_group, BbCreateView

urlpatterns = [
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:group_id>/', by_group, name='by_group'),
    path('', index, name='index'),
]
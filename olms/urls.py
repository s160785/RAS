from django.urls import path, include
from . import views

urlpatterns = [
    path('newleave', views.newLeave, name='newLeave'),
    path('', views.main, name='main_page'),
    path('home', views.home, name='home'),
    path('del/<int:lid>', views.delete, name='delete')
]

from django.urls import path, include
from . import views
from django.conf.urls import url
from django.conf import settings
from django.views.static import serve
from django.conf.urls.static import static

urlpatterns = [
    path('newleave', views.newLeave, name='newLeave'),
    path('', views.main, name='main_page'),
    path('home', views.home, name='home'),
    path('del/<int:lid>', views.delete, name='delete'),
    path('register', views.register, name='register'),
    url(r'^media/(?P<path>.*)$', serve,
        {'document_root': settings.MEDIA_ROOT}),
    url(r'^static/(?P<path>.*)$', serve,
        {'document_root': settings.STATIC_ROOT}),
    path('admin_home', views.admin_home, name='admin_home'),
    path('approve/<int:lid>', views.approve, name='approve'),
    path('reject/<int:lid>', views.reject, name='reject'),
    path('out/<int:lid>', views.out, name='out'),
    path('in/<int:lid>', views.inn, name='in'),
    path('sec_home', views.sec_home, name='sec_home'),

] + static(settings.STATIC_URL, doucument_root=settings.STATIC_ROOT)

urlpatterns += static(settings.MEDIA_URL,
                      document_root=settings.MEDIA_ROOT)

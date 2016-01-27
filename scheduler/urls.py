from django.conf.urls import url

from . import views


urlpatterns = [
    url(r'^(?P<slug>[\w-]+)/sign_up$', views.sign_up, name='sign_up'),
    url(r'^(?P<slug>[\w-]+)/sign_up/success$', views.sign_up_success, name='sign_up_success'),
]

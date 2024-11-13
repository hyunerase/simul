from flan.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path("kakao/login/", views.kakao_login, name="kakao_login"),
    path("kakao/callback/", views.kakao_callback, name="kakao_callback"),
]

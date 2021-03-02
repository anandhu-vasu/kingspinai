
from django.urls import path
from . import views
urlpatterns = [
path('',views.home,name="dashboard"),

path('register',views.Register,name="register"),
path('login',views.login_view,name="login"),
path('logout',views.logout_view,name="logout")

]

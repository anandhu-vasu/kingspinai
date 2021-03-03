from django.urls import path,include
from . import views

appname = 'chatbot'

dashboard_urlpatterns = [
    path('conversation-console',views.console,name='console'),
    path('',views.console,name='dashboard')
]

urlpatterns = [

    path('',views.index,name='index'),
    path('demo',views.console,name='console'),

    path('home',views.home,name="home"),
    path('show',views.show,name='show'),

    path('register',views.Register,name="register"),
    path('login',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),

    path('user/dashboard',include((dashboard_urlpatterns,appname),namespace="user"))
]

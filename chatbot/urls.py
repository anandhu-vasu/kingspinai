from django.urls import path,include
from . import views

appname = 'chatbot'

dashboard_urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('chatbots',views.chatbot,name='chatbot'),
    path('chatbot/<slug:name>/conversation-console',views.console,name='console'),
]

urlpatterns = [

    path('',views.index,name='index'),
    path('demo',views.demo,name='console'),

    path('home',views.home,name="home"),
    path('show',views.show,name='show'),

    path('register',views.Register,name="register"),
    path('login',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),

    path('user/dashboard/',include((dashboard_urlpatterns,appname),namespace="user"))
]

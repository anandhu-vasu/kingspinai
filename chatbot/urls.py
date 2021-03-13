from django.urls import path,include
from . import views
from chatbot.core.urls import api_urlpatterns

appname = 'chatbot'

dashboard_urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('chatbots/',views.chatbot,name='chatbot'),
    path('chatbot/<slug:name>/conversation-console/',views.console,name='console'),
]

urlpatterns = [

    path('',views.index,name='index'),
    path('demo',views.demo,name='console'),

    path('register',views.Register,name="register"),
    path('login',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),

    path('user',views.user,name="user"),
    path('user/dashboard/',include((dashboard_urlpatterns,appname),namespace="user")),
    path('api/',include((api_urlpatterns,appname),namespace="api"))
]

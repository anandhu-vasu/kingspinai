from django.urls import path,include
from . import views
from chatbot.core.urls import api_urlpatterns

appname = 'chatbot'

dashboard_urlpatterns = [
    path('',views.dashboard,name='dashboard'),
    path('chatbots/',views.chatbot,name='chatbot'),
    path('chatbot/<slug:name>/conversation-console/',views.console,name='console'),
    path('analytics',views.analytics,name='analytics'),
]

urlpatterns = [

    path('',views.index,name='index'),
    path('linguist',views.linguist,name="linguist"),
    path('multi-channel',views.multi_channel,name="multi-channel"),
    path('voice-enabled',views.voice_enabled,name="voice-enabled"),
    
          path('.well-known/pki-validation/30269148F03B43DFA891A56CB33FA529.txt', views.ssl_verify),


    path('register',views.Register,name="register"),
    path('login',views.login_view,name="login"),
    path('logout',views.logout_view,name="logout"),

    path('user',views.user,name="user"),
    path('user/dashboard/',include((dashboard_urlpatterns,appname),namespace="user")),
    path('api/',include((api_urlpatterns,appname),namespace="api"))
]

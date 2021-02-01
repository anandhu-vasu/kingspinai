from django.urls import path
from django.urls.conf import include
from . import views


platform_urlpatterns = [
    path('conversation-studio',views.conversationStudio,name='platform.conversation-studio')
]

urlpatterns = [
    path('',views.index,name='index'),
    path('why-kingspinai/',views.why,name='why-kingspinai'),
    path('platform/',include(platform_urlpatterns))
]
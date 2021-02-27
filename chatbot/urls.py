from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

dashboard_urlpatterns = [
    path('conversation-console',views.console,name='user.dashboard.console')
]

urlpatterns = [

    path('',views.index,name='index'),
    path('demo',views.console,name='console'),

    path('register',views.Register,name='register'),
    path('login',views.Login,name="login"),
    path('logout/',views.Logout,name='logout'),

    # path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),


    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="auth/forgot-password.html "),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),

    path('user/dashboard/',include(dashboard_urlpatterns),name="user.dashboard")
]
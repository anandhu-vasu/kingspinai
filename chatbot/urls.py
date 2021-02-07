from django.urls import path,include
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('index',views.index,name='index'),
    path('',views.Login,name="login"),

    path('register',views.Register,name='register'),
    path('login',views.Login,name="login"),
    path('logout/',views.Logout,name='logout'),

    # path('reset_password/',auth_views.PasswordResetView.as_view(),name="reset_password"),
    # path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(),name="password_reset_done"),
    # path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(),name="password_reset_confirm"),
    # path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(),name="password_reset_complete"),


    path('reset_password/',auth_views.PasswordResetView.as_view(template_name="password_reset.html "),name="reset_password"),
    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),name="password_reset_done"),
    path('reset/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),name="password_reset_confirm"),
    path('reset_password_complete/',auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),name="password_reset_complete"),


]
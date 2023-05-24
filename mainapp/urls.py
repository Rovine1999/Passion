from django.urls import include, path
from rest_framework import routers
from .views import *
from django.contrib.auth import views as auth_views

router = routers.DefaultRouter()

urlpatterns = [
    path('', home, name="home"),
    path('account/profile/', account_profile, name="account_profile"),
    path('account/profile/orders/', account_orders, name="account_orders"),
    path('about-us/', about, name='aboutus'),
    path('contact-us/', contactus, name='contactus'),
    path('frequentyl-asked-questions/', faq, name='faq'),

    path('login/', account_login, name='login'),
    path('logout/', account_logout, name='logout'),

    path('subscribe/', subscribe, name="subscribe"),

    # Password reset urls
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='agrul/pages/auth/password_reset.html'),
         name="password_reset"),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='agrul/pages/auth'
                                                                                        '/password_reset_done.html'),
         name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='agrul/pages/auth/password_reset_confirm.html'),
         name="password_reset_confirm"),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='agrul/pages/auth/password_reset_complete.html'),
         name="password_reset_complete"),

    #     Error Handling
    path("e404/", error404, name='error-404'),
    path("e500/", error500, name='error-500'),

    #   Get location coordinates
    path('location/coords/', get_coordinates, name='get_coordinates'),

    #   Terms and conditions
    path('terms-and-conditions/', tcs, name='tcs')
]

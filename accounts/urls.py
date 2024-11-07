# urls.py
from django.urls import path
from .views import signup_success,signup,verify_otp,profile

urlpatterns = [
    # Other URL patterns...
    path('signup/', signup, name='signup'),
    path('signup/success/', signup_success, name='signup_success'),
    path('verify-otp/', verify_otp, name='verify_otp'),
    path('profile/', profile, name='profile'),
]

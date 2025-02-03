from django.urls import path, include
from account.views import SignUpView, loginView, logoutView

app_name = 'account'
urlpatterns = [
    path('register', SignUpView.as_view(), name='register'),
    path('login', loginView, name='login'),
    path('logout', logoutView, name='logout'),
]
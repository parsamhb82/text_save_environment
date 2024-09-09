from django.urls import path
from .views import (Login,
                    Refresh,
                    UserRegistrationView,)

urlpatterns = [
    path('login/', Login.as_view()),
    path('refresh/', Refresh.as_view()),
    path('user-register/', UserRegistrationView.as_view()),
]
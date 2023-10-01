from django.urls import path
from .views import UserRegistrationView, UserLoginView, RideCreateView, RideDetailView, RideListView, RideAcceptView

urlpatterns = [
    path('register/', UserRegistrationView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('rides/create/', RideCreateView.as_view()),
    path('rides/<int:pk>/', RideDetailView.as_view()),
    path('rides/', RideListView.as_view()),
    path('rides/<int:pk>/accept/', RideAcceptView.as_view()),
]
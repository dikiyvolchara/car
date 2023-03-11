from django.urls import path

from .views import SingUpView, MyAccountView, ProfileUserCreateView, ProfileUserUpdateView, ProfileUserInformView

urlpatterns = [
    path('singup/', SingUpView.as_view(), name='singup'),
    path('my-account/<int:pk>/', MyAccountView.as_view(), name='my-account'),
    path('my-account/<int:pk>/create_profile/', ProfileUserCreateView.as_view(), name='profile_create'),
    path('my-account/<int:pk>/update', ProfileUserUpdateView.as_view(), name='update_inform'),
    path('my-account/inform/', ProfileUserInformView, name='user_inform')
]
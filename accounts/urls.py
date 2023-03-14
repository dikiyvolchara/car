from django.urls import path

from .views import SingUpView, MyAccountView, ProfileUserCreateView, ProfileUserUpdateView, ProfileUserInformView, ProfileUserDiscountView, ProfileUserManagerView

urlpatterns = [
    path('my-account/<int:pk>/create_profile/', ProfileUserCreateView.as_view(), name='profile_create'),
    path('my-account/<int:pk>/update', ProfileUserUpdateView.as_view(), name='update_inform'),
    path('my-account/manager/', ProfileUserManagerView, name='user_manager'),
    path('my-account/discount/', ProfileUserDiscountView, name='user_discount'),
    path('my-account/inform/', ProfileUserInformView, name='user_inform'),
    path('singup/', SingUpView.as_view(), name='singup'),
    #path('my-account/<int:pk>/', MyAccountView.as_view(), name='my-account'),
    path('my-account/', MyAccountView, name='my-account'),
]
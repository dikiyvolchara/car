from .forms import UserCreationForm, ProfileUserForm
from django.urls import reverse_lazy
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import ProfileUser
from django.views.generic import CreateView, DetailView, UpdateView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, UserPassesTestMixin

# Create your views here.
class SingUpView(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/singup.html'


@login_required
def MyAccountView(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'accounts/account.html', context)


# Create your views here.
# class MyAccountView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
#     model = User
#     template_name = 'accounts/account.html'

#     def test_func(self):
#         return self.get_object().id == self.request.user.pk or self.request.user.is_superuser

class ProfileUserCreateView(CreateView):
    form_class = ProfileUserForm

    success_url = reverse_lazy('/')
    template_name = 'accounts/create_profile.html'

    def form_valid(self, form):
        form.instance.user_profile = self.request.user
        return super(ProfileUserCreateView, self).form_valid(form)


    # def form_valid(self, form):
    #     obj = form.save(commit=False)
    #     obj.user_profile = self.request.user
    #     obj.save()

class ProfileUserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    # specify the model you want to use
    model = ProfileUser
  
    # specify the fields
    fields = [
        "city",
        "delivery",
        "birthday",
    ]
    template_name = 'accounts/update_inform.html'

    def test_func(self):
        return self.get_object().user_profile == self.request.user 
  
    # can specify success url
    # url to redirect after successfully
    # updating details
    success_url ="/"

@login_required
def ProfileUserInformView(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'accounts/accounts_inform.html', context)


@login_required
def ProfileUserDiscountView(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'accounts/account_discount.html', context)


@login_required
def ProfileUserManagerView(request):
    user = request.user

    context = {
        'user': user,
    }

    return render(request, 'accounts/account_manager.html', context)
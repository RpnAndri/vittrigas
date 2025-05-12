from django.views.generic import TemplateView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView
from django.contrib.auth import get_user_model

from . forms import UserCreateForm

User = get_user_model()



class Index(TemplateView):
    template_name = 'index.html'

class Login(LoginView):
    template_name = 'accounts/login.html'

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/signup.html'

class Profile(DetailView):
    context_object_name = 'profile'
    model = User
    template_name = 'accounts/profile.html'

    slug_field = 'username'
    slug_url_kwarg = 'username'



# class Success(TemplateView):
#     template_name = 'accounts/logged.html'
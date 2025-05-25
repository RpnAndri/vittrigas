from django.views.generic import TemplateView, CreateView, DetailView, ListView
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

# class Success(TemplateView):
#     template_name = 'accounts/logged.html'
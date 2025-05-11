from django.views.generic import TemplateView, CreateView
from django.urls import reverse_lazy

from . forms import UserCreateForm

class Index(TemplateView):
    template_name = 'index.html'

class SignUp(CreateView):
    form_class = UserCreateForm
    success_url = reverse_lazy('index')
    template_name = 'accounts/signup.html'
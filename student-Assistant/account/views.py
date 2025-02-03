from django.shortcuts import render
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
#from django.contrib.auth.forms import UserCreationForm
from account.forms import DoctorForm
from django.urls import reverse_lazy
from django.http import HttpResponse
from django.views.generic.edit import CreateView
from django.contrib.auth import  login, logout
from django.shortcuts import redirect
from django.contrib.auth.backends import ModelBackend
from django.contrib.auth import get_user_model
from .utils import authenticate
class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username) # Cambia 'username' por 'email' aqui
            if user.check_password(password):
                return user
        except UserModel.DoesNotExist:
            return None

# Create your views here.
class SignUpView(SuccessMessageMixin, CreateView):
    form_class = DoctorForm
    template_name = 'account/signup.html'
    success_url = reverse_lazy('account:login')
    success_message = "Your account was created successfully, please login"
    
    def form_valid(self, form):
        form.save()
        return super().form_valid(form)
    
   
    
def loginView(request):
    
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(email=email, password=password)
        if user is not None:
            login(request, user)
            
            return redirect('recording')  # Redirect to the home page
        else:
            return HttpResponse('Invalid Credentials')
    else:
        
        return render(request, 'account/login.html')

   
def logoutView(request):
    logout(request)
    return redirect('home')
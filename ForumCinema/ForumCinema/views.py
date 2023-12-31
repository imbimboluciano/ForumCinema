from django.shortcuts import render, redirect, HttpResponseRedirect
from .forms import UserCreationForm
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView
from django.http import HttpResponse   
from django.contrib.auth import login, authenticate, get_user_model
from django.contrib.sites.shortcuts import get_current_site  
from django.utils.encoding import * 
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode  
from django.template.loader import render_to_string  
from .token import account_activation_token  
from django.contrib.auth.models import User
from django.core.mail import EmailMessage 
from django.utils.encoding import force_bytes, force_str
from forum.models import Movie


def homepage(request):
    return render(request, template_name= "home.html")

  
def signup(request):  
    if request.method == 'POST':  
        form = UserCreationForm(request.POST)  
        if form.is_valid():  
            # save form in the memory not in database  
            user = form.save(commit=False)  
            user.is_active = False  
            user.save()  
                # to get the domain of the current site  
            current_site = get_current_site(request)  
            mail_subject = 'Activation link has been sent to your email id'  
            message = render_to_string('acc_active_email.html', {  
                'user': user,  
                'domain': current_site.domain,  
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),  
                'token':account_activation_token.make_token(user),  
            })  
            to_email = form.cleaned_data.get('email')  
            email = EmailMessage(mail_subject, message, to=[to_email])  
            email.send()  
            return redirect('login')  
    else:  
        form = UserCreationForm()  
    
    return render(request, 'registrazione.html', {'form': form})  



def activate(request, uidb64, token):  
    User = get_user_model()  
    try:  
        uid = force_str(urlsafe_base64_decode(uidb64))  
        user = User.objects.get(pk=uid)  
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):  
            user = None  
    if user is not None and account_activation_token.check_token(user, token):  
        user.is_active = True  
        user.save()
        return redirect("login")  
    else:  
        return HttpResponse('Activation link is invalid!')  
    

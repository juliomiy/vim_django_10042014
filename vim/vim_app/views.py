from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'vim_app/login_signup.html', None) 

def signup_main(request):
    return render(request, 'vim_app/signup_main.html', None) 

def signup_customer_main(request):
    return render(request, 'vim_app/signup_customer_main.html', None) 

def signup_stylist_main(request):
    return render(request, 'vim_app/signup_stylist_main.html', None) 

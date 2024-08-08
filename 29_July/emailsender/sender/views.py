from django.shortcuts import render, redirect
from django.http import HttpResponse
import logging
logger = logging.getLogger(__name__)
from django.contrib.auth import get_user_model
User = get_user_model()
from django.contrib import messages
from sender.emailer import sendTestEmail
import random

def index(request):
    # logger.info('This is a info msg')
    # logger.debug('This is a debugerror msg')
    # logger.error('This is a error msg')
    # logger.warning('This is a warning msg')
    # logger.critical('This is a critical msg')

    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')

        user_obj = User.objects.filter(phone_number = phone_number)

        if not user_obj.exists():
            messages.error(request, "Phone number is not registered.")
            return redirect('/')
        otp = random.randint(1000,9999)
        email = user_obj[0].email
        user_obj.update(otp=otp)
        subject= "otp for testing"
        message= f'Your otp for login is {otp}'

        sendTestEmail(email=email, subject=subject, message=message)
        return redirect(f'/check-otp/{user_obj.id}/')

        
   
    return render(request,'index.html')

def check_otp(request, user_id):
    print(user_id)


    return render(request,'check-otp.html')
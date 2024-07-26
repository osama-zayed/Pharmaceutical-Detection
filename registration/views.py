from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.models import User
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.contrib.auth import login

def logout_view(request):
    logout(request)
    return redirect('index')

def RegistrViews(request):
    form =SignUpForm
    return render(request,'registration/signup.html', {'form': form})

def signup(request):
    try:
        username = request.POST.get('username')
        password = request.POST.get('password1')
        confirm_password = request.POST.get('password2')
        email = request.POST.get('email')
        if not username or not password or not confirm_password or not email:
            messages.error(request, 'اسم المستخدم وكلمة المرور وتأكيد كلمة المرور والبريد الإلكتروني مطلوبة')
            return  redirect(request.META.get('HTTP_REFERER'))   

        if password != confirm_password:
            messages.error(request, 'كلمة المرور وتأكيد كلمة المرور غير متطابقتين')
            return  redirect(request.META.get('HTTP_REFERER'))
        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, 'عنوان البريد الإلكتروني غير صحيح')
            return  redirect(request.META.get('HTTP_REFERER'))
        user = User.objects.create_user(username=username, password=password, email=email)
        login(request, user)
        messages.success(request, 'تم تسجيل الدخول بنجاح')
        return redirect('index')

    except Exception :
        messages.error(request,'العملية فشلت')
        return  redirect(request.META.get('HTTP_REFERER'))  
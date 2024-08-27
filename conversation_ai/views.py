from django.shortcuts import render, redirect
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PromptForm
from .models import Prompt
from .gemeni import model
import time

@login_required
def index(request):
    prompts = Prompt.objects.filter(user=request.user)\
        .order_by('id')
    
    form = PromptForm()

    context = {
        'prompts': prompts
    }
    return render(request, 'index.html',context)

# Đăng nhập
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect("/")
        else:
            error = 'Tên tài khoản hoặc mật khẩu không chính xác'
            return render(request,'login.html', {"errors": error})
    return render(request, 'login.html')

#Đăng xuất
def user_logout(request):
    logout(request)
    return redirect("/")

# Đăng  ký
def user_signup(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        repeat_password = request.POST["repeat_password"]
        errors = {}

        if not username:
            errors['username'] = 'Tên đăng nhập không được để trống'

        elif not email:
            errors['email'] = 'Email không được để trống'
            
        elif not validate_email(email):
            errors["email"] = "Email không đúng định dạng"
            
        elif not password:
            errors['password'] = 'Mật khẩu không được để trống'
        
        elif not repeat_password:
            errors['repeat_password'] = 'Nhập lại mật khẩu không được để trống'
        
        elif password and repeat_password and password != repeat_password:
            errors['password_mismatch'] = 'Mật khẩu không khớp'
        
        if errors:
            messages = ""
            if errors:
                msg = []
                for key, mess in errors.items():
                    msg.append(mess+'\n')
                messages = ''.join(msg)
            return render(request, 'signup.html', {'errors': messages})
        else:
            try:
                user = User.objects.create_user(username,email,password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                return render(request, "signup.html", {"errors":'Lỗi khi tạo tài khoản'})
    return render(request, 'signup.html')

def addPrompt(request):
    if request.method == "POST":
        form = PromptForm(request.POST)
        if form.is_valid():
            prompt = form.save(commit=False)
            prompt.user = request.user
            prompt.username = request.user.username
            time.sleep(1)
            prompt.response = model.generate_content(prompt.prompt).text
            prompt.save()

            return redirect('/')
    else:
        form = PromptForm()

    context = {"form": form}
    return render(request, "index.html", context)

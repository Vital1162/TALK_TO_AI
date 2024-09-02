from django.shortcuts import render, redirect
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import PromptForm, Config
from .models import Prompt
from .gemeni import model
import time
from django.http import StreamingHttpResponse
from django.core.cache import cache


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

# def addPrompt(request):
#     if request.method == "POST":
#         form = PromptForm(request.POST)
#         config = Config(request.POST)
#         if form.is_valid():
#             prompt = form.save(commit=False)
#             prompt.user = request.user
#             prompt.username = request.user.username

#             # time.sleep(1)
#             # prompt.response = model.generate_content(prompt.prompt,
#             #                                          generation_config).text
#             # prompt.save()
#             return redirect('/')
#     else:
#         form = PromptForm()

#     context = {"form": form}
#     return render(request, "index.html", context)



from django.http import StreamingHttpResponse
def stream_response_view(request):
    prompt_text = request.GET.get('prompt', '')  # Get prompt from request
    user = request.user
    def content_generator(prompt_text):
        
        # generation_config = {
        #     "temperature": request.POST['temperature'],
        #     "top_p": request.POST['top_p'],
        #     "top_k": request.POST['top_k'],
        #     "max_output_tokens": request.POST['max_output_tokens'],
        # }
        # print(request.GET.get('top_p',''))
        
        chat_data = cache.get('adjustment')

        generation_config = {
            "temperature": float(chat_data.get("temperature")),
            "top_p": float(chat_data.get("top_p")),
            "top_k": int(chat_data.get("top_k")),
            "max_output_tokens": int(chat_data.get("max_output_tokens")),
        }
        
        print(generation_config)
        response = model.generate_content(prompt_text, stream=True,
                                          generation_config=generation_config)
        for chunk in response:
            if chunk.text:
                yield chunk.text
        yield "\n"  # Ensure the stream ends with a newline for clarity
        
        prompt = Prompt(user=user,prompt=prompt_text, response=response.text)
        prompt.save()
    
    return StreamingHttpResponse(content_generator(prompt_text), content_type='text/plain')

        
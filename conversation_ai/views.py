from django.shortcuts import render, redirect
from email_validator import validate_email, EmailNotValidError
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from .gemeni import model
import time
from django.http import StreamingHttpResponse
from django.core.cache import cache
from django.utils import timezone # need for get time


@login_required
def index(request):
    conversations = Conversation.objects.filter(user=request.user).order_by('-start_time')
    context = {
        'conversations': conversations,
    }
    return render(request, 'index.html', context)


# Đăng nhập
def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
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
                user = User.objects.create_user(username, email, password)
                user.save()
                login(request, user)
                return redirect('/')
            except:
                return render(request, "signup.html", {"errors": 'Lỗi khi tạo tài khoản'})
    return render(request, 'signup.html')


from django.http import StreamingHttpResponse
def stream_response_view(request):

    prompt_text = request.GET.get('prompt', '')  # Get prompt from request
    conversation_id = request.GET.get('conversation_id')

    user = request.user

    def content_generator(prompt_text):
        chat_data = cache.get('adjustment')

        generation_config = {
            "temperature": float(chat_data.get("temperature")),
            "top_p": float(chat_data.get("top_p")),
            "top_k": int(chat_data.get("top_k")),
            "max_output_tokens": int(chat_data.get("max_output_tokens")),
        }

        response = model.generate_content(prompt_text, stream=True, generation_config=generation_config)

        for chunk in response:
            if chunk.text:
                yield chunk.text
        yield "\n"  # Ensure the stream ends with a newline for clarity

        
        
        if conversation_id:
            conversation = Conversation.objects.get(id=conversation_id)
        else:
            conversation = Conversation.objects.create(user=user, start_time=timezone.now())
            
        # Save the prompt and response to the Prompt model
        prompt = Prompt(conversation=conversation, user=user, prompt=prompt_text, response=response.text, timestamp=timezone.now())
        prompt.save()
        
        conversation.end_time = timezone.now()
        conversation.save()
        # Save the conversation, but create a local instance, not global
        # conversation = Conversation(user=user, start_time=timezone.now(), end_time=timezone.now())
        
        if not conversation.response:
            sumary = f"""
            ##Instruction
            create title only text don't include any special character like '#' for this sentence
            #Sentence
            {prompt_text}
            #Title
            
            """
            conversation.response = model.generate_content(sumary, generation_config={'max_output_tokens': 5}).text
            conversation.save()

    return StreamingHttpResponse(content_generator(prompt_text), content_type='text/plain')



from chess import Board
def chess(request):
    board = Board()
    board_fen = board.board_fen()
    
    return render(request, 'chess.html', {'board_fen': board_fen})


from django.http import JsonResponse

def get_conversation(request, conversation_id):
    conversation = Conversation.objects.get(id=conversation_id, user=request.user)
    prompts = conversation.prompts.all().order_by('timestamp')
    data = {
        'id': conversation.id,
        'start_time': conversation.start_time,
        'end_time': conversation.end_time,
        'prompts': [{'prompt': p.prompt, 'response': p.response, 'timestamp': p.timestamp} for p in prompts]
    }
    return JsonResponse(data)

# from django.http import JsonResponse
# from django.views.decorators.http import require_POST

# @login_required
# def get_conversations(request):
#     conversations = Conversation.objects.filter(user=request.user).order_by('-start_time')
#     data = {
#         'conversations': [
#             {
#                 'id': c.id,
#                 'title': c.title,
#                 'start_time': c.start_time,
#                 'is_active': c.is_active
#             } for c in conversations
#         ]
#     }
#     return JsonResponse(data)

# @login_required
# def get_conversation(request, conversation_id):
#     conversation = Conversation.objects.get(id=conversation_id, user=request.user)
#     prompts = conversation.prompts.all().order_by('timestamp')
#     data = {
#         'id': conversation.id,
#         'title': conversation.title,
#         'start_time': conversation.start_time,
#         'end_time': conversation.end_time,
#         'prompts': [{'prompt': p.prompt, 'response': p.response, 'timestamp': p.timestamp} for p in prompts]
#     }
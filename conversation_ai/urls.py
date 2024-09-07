from . import views
from django.urls import path

urlpatterns = [
    path('',views.index, name="index"),
    path('login',views.user_login, name="login"),
    path('signup',views.user_signup, name="signup"),
    path('logout',views.user_logout, name="logout"),
    path('stream_response/', views.stream_response_view, name='stream_response'),
    path('chess_ai', views.chess, name="chess_ai"),
    path('get_conversation/<int:conversation_id>/', views.get_conversation, name='get_conversation'),

]

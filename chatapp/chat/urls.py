from django.urls import path , include
from django.urls import re_path
from . import consumers
from . import views 
urlpatterns = [
    #    path('', views.home, name='home'),
    #    path('signup/', views.signup_view, name='signup'),  # Signup page URL
    #    path('login/', views.login_page, name='login'),
    path('chat/<str:room_name>/', views.chat, name='chat'),
    ]

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<username>\w+)/$', consumers.ChatConsumer.as_asgi()),
]
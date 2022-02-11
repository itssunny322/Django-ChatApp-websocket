from .views import *
from django.urls import path,include
from django.conf.urls import url,re_path

urlpatterns = [
    path("home1",home1,name="home"),
    path('registration/', sign_up, name='sign_up'),
    path('login/', LoginView.as_view(), name='login'),
    path('list/users/',users, name='users'),
    # path(r'login/', log_in, name='login'),
    path('', signup, name='signup'),
    path('home/', home, name='home'),
    path('chatMessage/', ChatMessageListView.as_view()),
    path('chatMessage/<pk>/', ChatMessageDetailView.as_view()),
    path("inbox", InboxView.as_view()),
    re_path(r"^messages/(?P<username>[\w.@+-]+)", ThreadView.as_view()),

]
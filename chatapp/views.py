from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import *
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.generics import ListAPIView, RetrieveAPIView
from django.contrib.auth.models import User
from django.http import JsonResponse


from .forms import ComposeForm
from .models import Thread, ChatMessage
from django.contrib.auth.models import User

from django.views import generic
from django.views.generic import View

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import Http404, HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic.edit import FormMixin
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import DetailView, ListView

from .forms import *
from .models import Thread, ChatMessage
from django.contrib.auth.models import User

from django.views import generic
from django.views.generic import View



# Create your views here.
def home1(request):
    return render ( request,'home1.html')


#api for user registration
@api_view(['POST'])
def sign_up(request):
        serialized = UserSerializer(data=request.data)

        if serialized.is_valid():
            user=User.objects.create_user(
                serialized.data['username'],
                serialized.data['email'],
                serialized.data['password'],

            )
            user.save()
            return Response(serialized.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)


#api for use login
# @permission_classes([permissions.AllowAny,])
class LoginView(APIView):
    def post(self, request, format=None):
        data = request.data

        username = data.get('username', None)
        password = data.get('password', None)
        user = authenticate(username=username, password=password)

        if user is not None:
            token, _ = Token.objects.get_or_create(user=user)
            if user.is_active:
                login(request, user)
                context = {
                    'user_id': user.id,
                    'user': user.email,
                    'token': token.key,

                }
                return Response(context, status=status.HTTP_200_OK)
            else:
                return Response({"Msg ': 'User isn't active "}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"Msg ': 'Invalid username/password"}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def users(request):
    users = User.objects.all().values()
    return JsonResponse ({"Users": list(users)})



def signup(request):
    if request.method == 'POST':
        form = SignUpForms(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForms()
    return render(request, 'signup.html', {'form': form})

def log_in(request):
    if request.method == 'POST':
        form = LoginForms(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = LoginForms()
    return render(request,'login.html',{'form':form})

def home(request):
    users = User.objects.values()
    return render(request, 'home.html', {'users':users})


class ChatMessageListView(ListAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer

class ChatMessageDetailView(RetrieveAPIView):
    queryset = ChatMessage.objects.all()
    serializer_class = ChatMessageSerializer


class InboxView(LoginRequiredMixin, ListView):
    template_name = 'inbox.html'
    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)


class ThreadView(LoginRequiredMixin, FormMixin, DetailView):
    template_name = 'thread.html'
    form_class = ComposeForm
    success_url = './'

    def get_queryset(self):
        return Thread.objects.by_user(self.request.user)

    def get_object(self):
        other_username  = self.kwargs.get("username")
        print(self.request.user)
        print(other_username)
        obj, created    = Thread.objects.get_or_new(self.request.user, other_username)
        if obj == None:
            raise Http404
        return obj

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = self.get_form()
        return context

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        self.object = self.get_object()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        users = User.objects.values()
        return render(request, 'thread.html', {'users':users})

    def form_valid(self, form):
        thread = self.get_object()
        user = self.request.user
        message = form.cleaned_data.get("message")
        ChatMessage.objects.create(user=user, thread=thread, message=message)
        return super().form_valid(form)

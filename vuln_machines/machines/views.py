from django.shortcuts import render, redirect
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
import logging
from .models import VulnerableMachine
from .forms import VulnerableMachineForm
from .models import VulnerableMachine
from .serializers import VulnerableMachineSerializer
from rest_framework import generics, permissions
from .serializers import RegisterSerializer
from django.contrib.auth.models import User
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

logger = logging.getLogger(__name__)

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

class IsAdminOrCreator(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.is_staff or obj.creator == request.user

class VulnerableMachineViewSet(viewsets.ModelViewSet):
    queryset = VulnerableMachine.objects.all()
    serializer_class = VulnerableMachineSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrCreator]
    
    def create(self, request, *args, **kwargs):
        logger.info(f"Получен запрос на создание машины: {request.data}")
        try:
            return super().create(request, *args, **kwargs)
        except Exception as e:
            logger.error(f"Ошибка при создании машины: {e}")
            return Response(
                {"error": str(e)}, 
                status=status.HTTP_400_BAD_REQUEST
            )

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user)

class CurrentUserView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        return Response({
            'username': user.username,
            'is_staff': user.is_staff,
        })

def machine_list(request):
    machines = VulnerableMachine.objects.all().order_by('-created_at')
    return render(request, 'machines/list.html', {'machines': machines})

def add_machine(request):
    if request.method == 'POST':
        form = VulnerableMachineForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('machine_list')
    else:
        form = VulnerableMachineForm()
    
    return render(request, 'machines/add.html', {'form': form})

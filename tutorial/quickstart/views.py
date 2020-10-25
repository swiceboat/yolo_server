from django.shortcuts import render
from django.contrib.auth.models import User, Group
#from rest_framework.decorators import action
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets,status,generics
from .serializers import UserSerializer, GroupSerializer
from .serializers import InferenceSerializer
from .models import Inference
from celery.result import AsyncResult

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class InferenceViewSet(viewsets.ModelViewSet):
    serializer_class = InferenceSerializer
    queryset = Inference.objects.all()
    
    @api_view(['GET'])   
    def monitor_inference_progress(self,request,slug):
        inference_obj = self.get_object()
        progress = 100
        result  = AsyncResult(inference_obj.task_id)
        if isinstance(result.info, dict):
            progress  = result.info['progress']
        description = result.state
        return Response({'progress':progress,'description':description},status=status.HTTP_200_OK)

from rest_framework import viewsets, permissions
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Hackathon, Submission
from core.serializers import HackathonSerializer, SubmissionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.authentication import SessionAuthentication, TokenAuthentication

from django.http import JsonResponse

class HackathonViewSet(viewsets.ModelViewSet):
    serializer_class = HackathonSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Hackathon.objects.filter(associated_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(associated_user=self.request.user)

    def list(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(associated_user=self.request.user)
        return Response(serializer.data, status=201)

    def retrieve(self, request, id):
        print(id)
        queryset = self.get_queryset()
        hackathon = get_object_or_404(queryset, id=id)
        serializer = self.get_serializer(hackathon)
        return Response(serializer.data)

    def update(self, request, id=None):
        queryset = self.get_queryset()
        hackathon = get_object_or_404(queryset, id=id)
        serializer = self.get_serializer(hackathon, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def destroy(self, request, id=None):
        queryset = self.get_queryset()
        hackathon = get_object_or_404(queryset, id=id)
        hackathon.delete()
        return Response(status=204)
    
    def all_submissions(self, request, id):
        queryset = Submission.objects.filter(hackathon_id=id)
        data = {
            'status_code': 200,
            'submissions' : [ sub.get_submission_data() for sub in queryset]
        }
        return Response(data)
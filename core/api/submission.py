from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from core.models import Hackathon, Submission
from core.serializers import HackathonSerializer, SubmissionSerializer
from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, TokenAuthentication



class SubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = SubmissionSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = (TokenAuthentication, SessionAuthentication)

    def get_queryset(self):
        return Submission.objects.filter(associated_user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(associated_user=self.request.user)

    def hackathon_details(self, request):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(associated_user=self.request.user)
        return Response(serializer.data, status=201)

    def retrieve(self, request, id):
        queryset = Submission.objects.filter(hackathon_id=id)
        data = {
            'status_code': 200,
            'submisiions' : [ sub.get_submission_data() for sub in queryset]
        }
        return Response(data)

    def update(self, request, id=None):
        queryset = self.get_queryset()
        submission = get_object_or_404(queryset, id=id)
        serializer = self.get_serializer(submission, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=400)
        
    def destroy(self, request, id=None):
        queryset = self.get_queryset()
        submission = get_object_or_404(queryset, id=id)
        submission.delete()
        return Response(status=204)
    

    
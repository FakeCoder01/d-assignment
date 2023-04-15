from rest_framework import serializers
from .models import Hackathon, Submission

class HackathonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hackathon
        fields = ["id", "title", "description", "background_image", "hackathon_image", "type_of_submission", "start_time", "end_time", "reward_prize", "updated_at", "created_at", "associated_user"]
        # fields = "__all__"

class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:

        model = Submission
        fields = ["id", "hackathon_id", "name", "summary", "file", "link", "image", "updated_at", "created_at", "associated_user"]
        # fields = "__all__"

     
from django.db import models
import uuid
from django.contrib.auth.models import User


# Create your models here.

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True, editable=False)
    updated_at = models.DateTimeField(auto_now_add=True)
    created_at = models.DateField(auto_now=True)
    associated_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="associated_user", editable=False)


SUBMISSION_TYPES = [
    ("link", "link"),
    ("image", "image"),
    ("file", "file")
]


class Hackathon(BaseModel):
    title = models.CharField(max_length=50)
    description = models.TextField()

    background_image = models.ImageField(upload_to="background_images/", null=True, blank=True)
    hackathon_image = models.ImageField(upload_to="hackathon_thumbnails/", null=True, blank=True)

    type_of_submission = models.CharField(max_length=5, choices=SUBMISSION_TYPES, default="link")
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    reward_prize = models.CharField(max_length=200)

    

    def __str__(self) -> str:
        return self.title
    
    def get_formated_datetime(self):
        return {
            "start" : self.start_time.strftime("%H:%M , %B %d, %Y"),
            "end" : self.end_time.strftime("%H:%M , %B %d, %Y"),
        }
    

    
class Submission(BaseModel):
    
    hackathon_id = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name="submitted_hackathon")

    name = models.CharField(max_length=100)
    summary = models.TextField()

    file = models.FileField(upload_to="submissions/files/", null=True, blank=True)
    link = models.URLField(null=True, blank=True)
    image = models.ImageField(upload_to="submissions/images/", null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    def get_submission_data(self):

        if self.hackathon_id.type_of_submission == "link":
            submission_url = self.link
        elif self.hackathon_id.type_of_submission == "file":
            submission_url = self.file
        else:
            submission_url = self.image

        return {
            "user" : (self.associated_user.id),
            "hackathon" : str(self.hackathon_id.id),
            "submitted_on" : self.created_at,
            "submission_type" : self.hackathon_id.type_of_submission,
            "name" : self.name,
            "summary" : self.summary,
            "submission_url" : submission_url
        }
    

# https://meet.google.com/hwk-wpjp-tce    
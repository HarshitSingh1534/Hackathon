from django.contrib.auth.models import User
from django.db import models


class Hackathon(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    background_image = models.ImageField(upload_to='hackathons/backgrounds/')
    hackathon_image = models.ImageField(upload_to='hackathons/images/')
    type_of_submission = models.CharField(max_length=10, choices=[('image', 'Image'), ('file', 'File'), ('link', 'Link')])
    start_datetime = models.DateTimeField()
    end_datetime = models.DateTimeField()
    reward_prize = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hackathons_created')

    def __str__(self):
        return self.title


class Submission(models.Model):
    hackathon = models.ForeignKey(Hackathon, on_delete=models.CASCADE, related_name='submissions')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='submissions')
    submission_name = models.CharField(max_length=100)
    summary = models.TextField()

    image_submission = models.ImageField(upload_to='submissions/images/', blank=True, null=True)
    file_submission = models.FileField(upload_to='submissions/files/', blank=True, null=True)
    link_submission = models.URLField(blank=True)

    def __str__(self):
        return f'{self.submission_name} - {self.hackathon.title}'


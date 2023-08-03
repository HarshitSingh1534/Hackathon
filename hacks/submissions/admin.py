from django.contrib import admin
from .models import Hackathon, Submission


# Register your models here.
@admin.register(Hackathon)
class HackathonAdmin(admin.ModelAdmin):
    list_display = ['title', 'description', 'background_image', 'hackathon_image', 'type_of_submission',
                    'start_datetime', 'end_datetime', 'reward_prize', 'created_by']


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ['hackathon', 'user', 'submission_name', 'summary', ]

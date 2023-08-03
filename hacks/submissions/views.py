from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import UserRegistrationForm, HackathonForm, SubmissionForm
from .models import Hackathon, Submission
from django.contrib.auth.decorators import login_required
from django.utils import timezone


def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserRegistrationForm()
    return render(request, 'register.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def dashboard(request):
    user_hackathons = Hackathon.objects.filter(created_by=request.user)
    user_submissions = Submission.objects.filter(user=request.user)
    context = {
        'user_hackathons': user_hackathons,
        'user_submissions': user_submissions,
        'user': request.user,
    }

    return render(request, 'dashboard.html', context)


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
def all_hackathons(request):
    hackathons = Hackathon.objects.filter(end_datetime__gt=timezone.now())
    return render(request, 'all_hackathons.html', {'hackathons': hackathons})


@login_required
def hackathon_detail(request, hackathon_id):
    hackathon = Hackathon.objects.get(pk=hackathon_id)
    return render(request, 'hackathon_detail.html', {'hackathon': hackathon})


@login_required
def register_for_hackathon(request, hackathon_id):
    hackathon = Hackathon.objects.get(pk=hackathon_id)

    current_time = timezone.now()
    if current_time < hackathon.start_datetime or current_time > hackathon.end_datetime:
        return render(request, 'submit_to_hackathon_error.html', {'hackathon': hackathon})

    if Submission.objects.filter(hackathon=hackathon, user=request.user).exists():
        return render(request, 'already_registered.html', {'hackathon': hackathon})

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.hackathon = hackathon
            submission.user = request.user

            if submission.submission_type != hackathon.type_of_submission:
                return render(request, 'invalid_submission_type.html', {'hackathon': hackathon})

            submission.save()
            return redirect('my_hackathons')
    else:
        form = SubmissionForm()
    return render(request, 'register_for_hackathon.html', {'form': form, 'hackathon': hackathon})


@login_required
def create_hackathon(request):
    if request.method == 'POST':
        form = HackathonForm(request.POST, request.FILES)
        if form.is_valid():
            new_hackathon = form.save(commit=False)
            new_hackathon.created_by = request.user
            new_hackathon.save()
            return redirect('my_hackathons')
    else:
        form = HackathonForm()
    return render(request, 'create_hackathon.html', {'form': form})


@login_required
def submit_to_hackathon(request, hackathon_id):
    hackathon = get_object_or_404(Hackathon, pk=hackathon_id)

    if request.user not in hackathon.registered_users.all():
        return render(request, 'submit_to_hackathon_error.html',
                      {'hackathon': hackathon, 'error_message': 'You are not registered for this hackathon.'})

    current_time = timezone.now()
    if current_time < hackathon.start_datetime or current_time > hackathon.end_datetime:
        return render(request, 'submit_to_hackathon_error.html', {'hackathon': hackathon,
                                                                  'error_message': 'You can only submit to the hackathon between {} and {}.'.format(
                                                                      hackathon.start_datetime,
                                                                      hackathon.end_datetime)})
    if Submission.objects.filter(hackathon=hackathon, user=request.user).exists():
        return render(request, 'already_submitted.html', {'hackathon': hackathon})

    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.hackathon = hackathon
            submission.user = request.user
            submission.save()
            return redirect('my_hackathons')
    else:
        form = SubmissionForm()
    return render(request, 'submit_to_hackathon.html', {'form': form, 'hackathon': hackathon})


@login_required
def my_hackathons(request):
    user_hackathons = Hackathon.objects.filter(created_by=request.user)
    return render(request, 'my_hackathons.html', {'user_hackathons': user_hackathons})


def home_page(request):
    return render(request, 'HomePage.html')

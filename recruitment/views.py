from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Candidate, Position, Interview, Application
from .forms import CandidateForm, CandidateRegistrationForm, ApplicationForm, PositionForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required

def home(request):
    upcoming_interviews = Interview.objects.filter(
        scheduled_date__gte=timezone.now(),
        status='scheduled'
    ).order_by('scheduled_date')[:5]
    
    open_positions = Position.objects.filter(is_active=True)
    
    # Get counts for stats
    candidates_count = Candidate.objects.count()
    interviews_count = Interview.objects.count()
    open_positions_count = open_positions.count()
    
    context = {
        'upcoming_interviews': upcoming_interviews,
        'open_positions': open_positions,
        'candidates_count': candidates_count,
        'interviews_count': interviews_count,
        'open_positions_count': open_positions_count,
    }
    return render(request, 'recruitment/home.html', context)

@login_required
def interview_list(request):
    interviews = Interview.objects.all().order_by('-scheduled_date')
    return render(request, 'recruitment/interview_list.html', {'interviews': interviews})

@login_required
def candidate_list(request):
    candidates = Candidate.objects.all().order_by('-created_at')
    return render(request, 'recruitment/candidate_list.html', {'candidates': candidates})

@login_required
@staff_member_required
def position_list(request):
    """View for staff to manage job positions"""
    positions = Position.objects.all().order_by('-id')
    return render(request, 'recruitment/position_list.html', {
        'positions': positions,
    })

@login_required
def candidate_detail(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    interviews = Interview.objects.filter(candidate=candidate)
    return render(request, 'recruitment/candidate_detail.html', {
        'candidate': candidate,
        'interviews': interviews
    })

@login_required
def candidate_create(request):
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f"Candidate {candidate.name} was created successfully.")
            return redirect('recruitment:candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm()
    
    return render(request, 'recruitment/candidate_form.html', {'form': form, 'title': 'Add New Candidate'})

@login_required
def candidate_edit(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    
    if request.method == "POST":
        form = CandidateForm(request.POST, request.FILES, instance=candidate)
        if form.is_valid():
            candidate = form.save()
            messages.success(request, f"Candidate {candidate.name} was updated successfully.")
            return redirect('recruitment:candidate_detail', pk=candidate.pk)
    else:
        form = CandidateForm(instance=candidate)
    
    return render(request, 'recruitment/candidate_form.html', {
        'form': form, 
        'title': 'Edit Candidate',
        'candidate': candidate
    })

@login_required
def candidate_delete(request, pk):
    candidate = get_object_or_404(Candidate, pk=pk)
    
    if request.method == "POST":
        candidate_name = candidate.name
        candidate.delete()
        messages.success(request, f"Candidate {candidate_name} was deleted successfully.")
        return redirect('recruitment:candidate_list')
    
    return render(request, 'recruitment/candidate_confirm_delete.html', {'candidate': candidate})


def register(request):
    if request.method == 'POST':
        form = CandidateRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. You can now apply for positions.")
            return redirect('recruitment:position_list')
    else:
        form = CandidateRegistrationForm()
    return render(request, 'recruitment/register.html', {'form': form})

@login_required
def candidate_profile(request):
    try:
        candidate = Candidate.objects.get(user=request.user)
        applications = Application.objects.filter(candidate=candidate)
        interviews = Interview.objects.filter(candidate=candidate)
        
        return render(request, 'recruitment/candidate_profile.html', {
            'candidate': candidate,
            'applications': applications,
            'interviews': interviews
        })
    except Candidate.DoesNotExist:
        messages.error(request, "Candidate profile not found.")
        return redirect('recruitment:home')

def public_position_detail(request, pk):
    position = get_object_or_404(Position, pk=pk)
    
    # Check if the user has already applied
    already_applied = False
    if request.user.is_authenticated and hasattr(request.user, 'candidate'):
        already_applied = Application.objects.filter(
            candidate=request.user.candidate,
            position=position
        ).exists()
    
    if request.user.is_authenticated and request.method == 'POST' and not already_applied and hasattr(request.user, 'candidate'):
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = Application(
                candidate=request.user.candidate,
                position=position,
                cover_letter=form.cleaned_data['cover_letter'],
                resume=form.cleaned_data['resume']
            )
            application.save()
            messages.success(request, f"You have successfully applied for {position.title}")
            return redirect('recruitment:candidate_profile')
    else:
        form = ApplicationForm()
    
    return render(request, 'recruitment/public_position_detail.html', {
        'position': position,
        'form': form,
        'already_applied': already_applied,
        'user_authenticated': request.user.is_authenticated
    })

def public_position_list(request):
    positions = Position.objects.filter(is_active=True)
    return render(request, 'recruitment/public_position_list.html', {'positions': positions})


def is_hr_staff(user):
    return hasattr(user, 'profile') and user.profile.user_type in ['hr', 'admin']

def is_interviewer(user):
    return hasattr(user, 'profile') and user.profile.user_type in ['interviewer', 'admin']

def staff_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None and hasattr(user, 'profile') and user.profile.user_type in ['hr', 'interviewer', 'admin']:
            login(request, user)
            messages.success(request, f"Welcome back, {user.get_full_name() or user.username}!")
            return redirect('recruitment:home')
        else:
            messages.error(request, "Invalid login credentials or insufficient permissions.")
    
    return render(request, 'recruitment/staff_login.html')

@login_required
@user_passes_test(is_hr_staff)
def hr_dashboard(request):
    # Get stats for HR dashboard
    active_positions_count = Position.objects.filter(is_active=True).count()
    pending_applications_count = Application.objects.filter(status='pending').count()
    upcoming_interviews_count = Interview.objects.filter(
        scheduled_date__gte=timezone.now(),
        status='scheduled'
    ).count()
    
    # Get recent applications
    recent_applications = Application.objects.all().order_by('-created_at')[:10]
    
    context = {
        'active_positions_count': active_positions_count,
        'pending_applications_count': pending_applications_count,
        'upcoming_interviews_count': upcoming_interviews_count,
        'recent_applications': recent_applications,
    }
    
    return render(request, 'recruitment/hr_dashboard.html', context)

@login_required
@user_passes_test(is_interviewer)
def interviewer_dashboard(request):
    # Interviewer specific dashboard
    return render(request, 'recruitment/interviewer_dashboard.html')


def logout_view(request):
    logout(request)
    return redirect('recruitment:home')


@login_required
@staff_member_required
def position_create(request):
    """View for staff to create a new job position"""
    if request.method == 'POST':
        form = PositionForm(request.POST)
        if form.is_valid():
            position = form.save()
            messages.success(request, f"Position '{position.title}' created successfully.")
            return redirect('recruitment:position_list')
    else:
        form = PositionForm()
    
    return render(request, 'recruitment/position_form.html', {
        'form': form,
        'title': 'Create Position',
        'button_text': 'Create'
    })

@login_required
@staff_member_required
def position_edit(request, pk):
    """View for staff to edit an existing job position"""
    position = get_object_or_404(Position, pk=pk)
    
    if request.method == 'POST':
        form = PositionForm(request.POST, instance=position)
        if form.is_valid():
            position = form.save()
            messages.success(request, f"Position '{position.title}' updated successfully.")
            return redirect('recruitment:position_list')
    else:
        form = PositionForm(instance=position)
    
    return render(request, 'recruitment/position_form.html', {
        'form': form,
        'position': position,
        'title': 'Edit Position',
        'button_text': 'Update'
    })

@login_required
@staff_member_required
def position_toggle(request, pk):
    """View for staff to toggle position active status"""
    position = get_object_or_404(Position, pk=pk)
    position.is_active = not position.is_active
    position.save()
    
    status = "activated" if position.is_active else "deactivated"
    messages.success(request, f"Position '{position.title}' {status} successfully.")
    return redirect('recruitment:position_list')


@login_required
@staff_member_required
def position_detail(request, pk):
    """View for staff to see details of a job position"""
    position = get_object_or_404(Position, pk=pk)
    applications = Application.objects.filter(position=position)
    
    return render(request, 'recruitment/position_detail.html', {
        'position': position,
        'applications': applications,
    })

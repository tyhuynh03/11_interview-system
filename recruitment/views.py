from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.utils import timezone
from .models import Candidate, Position, Interview, Application
from .forms import CandidateForm, CandidateRegistrationForm, ApplicationForm, PositionForm, InterviewScheduleForm
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, JsonResponse
import csv
from datetime import datetime, timedelta
from .models import Application, ApplicationStatusHistory, Position
from django.urls import reverse

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
            # Đăng nhập người dùng sau khi đăng ký
            login(request, user)
            # Chuyển hướng đến trang danh sách vị trí công việc thay vì trang admin
            return redirect('recruitment:public_position_list')
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
    
    # Search functionality
    search_query = request.GET.get('search', '')
    if search_query:
        positions = positions.filter(
            Q(title__icontains=search_query) | 
            Q(description__icontains=search_query) |
            Q(requirements__icontains=search_query)
        )
    
    # Department filter
    department = request.GET.get('department', '')
    if department:
        positions = positions.filter(department=department)
    
    # Employment type filter
    employment_type = request.GET.get('employment_type', '')
    if employment_type:
        positions = positions.filter(employment_type=employment_type)
    
    # Sorting
    sort_by = request.GET.get('sort', 'title')
    if sort_by == 'title':
        positions = positions.order_by('title')
    elif sort_by == 'department':
        positions = positions.order_by('department', 'title')
    elif sort_by == 'newest':
        positions = positions.order_by('-id')  # Assuming newer positions have higher IDs
    
    # Pagination
    paginator = Paginator(positions, 9)  # Show 9 positions per page
    page = request.GET.get('page')
    try:
        positions = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        positions = paginator.page(1)
    except EmptyPage:
        # If page is out of range, deliver last page of results.
        positions = paginator.page(paginator.num_pages)
    
    # Get unique departments for filter dropdown
    departments = Position.objects.filter(is_active=True).exclude(
        department__isnull=True).exclude(department='').values_list(
        'department', flat=True).distinct()
    
    # Get employment types for filter dropdown
    employment_types = Position.EMPLOYMENT_TYPES
    
    context = {
        'positions': positions,
        'departments': departments,
        'employment_types': employment_types,
        'current_sort': sort_by,
    }
    
    return render(request, 'recruitment/public_position_list.html', context)


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


# Thêm các import cần thiết
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse
import csv
from datetime import datetime
from .models import Application, ApplicationStatusHistory, Position

@login_required
@user_passes_test(is_hr_staff)
def application_management(request):
    """View for HR staff to manage job applications"""
    applications = Application.objects.all().order_by('-created_at')
    
    # Get all active positions for filter dropdown
    positions = Position.objects.filter(is_active=True)
    
    # Filter by position
    selected_position = request.GET.get('position', '')
    if selected_position:
        applications = applications.filter(position_id=selected_position)
    
    # Filter by status
    selected_status = request.GET.get('status', '')
    if selected_status:
        applications = applications.filter(status=selected_status)
    
    # Search by candidate name or email
    search_query = request.GET.get('search', '')
    if search_query:
        applications = applications.filter(
            Q(candidate__name__icontains=search_query) | 
            Q(candidate__email__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(applications, 10)  # Show 10 applications per page
    page = request.GET.get('page')
    try:
        applications = paginator.page(page)
    except PageNotAnInteger:
        applications = paginator.page(1)
    except EmptyPage:
        applications = paginator.page(paginator.num_pages)
    
    context = {
        'applications': applications,
        'positions': positions,
        'status_choices': Application.STATUS_CHOICES,
        'selected_position': selected_position,
        'selected_status': selected_status,
        'search_query': search_query,
    }
    
    return render(request, 'recruitment/application_management.html', context)

@login_required
@user_passes_test(is_hr_staff)
def application_detail(request, pk):
    """View for HR staff to see details of a job application"""
    application = get_object_or_404(Application, pk=pk)
    application_history = application.status_history.all()
    
    context = {
        'application': application,
        'application_history': application_history,
        'status_choices': Application.STATUS_CHOICES,
    }
    
    return render(request, 'recruitment/application_detail.html', context)

@login_required
@user_passes_test(is_hr_staff)
def update_application_status(request, pk):
    """View for HR staff to update application status"""
    application = get_object_or_404(Application, pk=pk)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        notes = request.POST.get('notes', '')
        
        if new_status and new_status != application.status:
            # Create history record
            ApplicationStatusHistory.objects.create(
                application=application,
                previous_status=application.status,
                new_status=new_status,
                notes=notes,
                updated_by=request.user
            )
            
            # Update application status
            application.status = new_status
            application.save()
            
            messages.success(request, f"Application status updated to {application.get_status_display()}")
        
        # Redirect back to the referring page
        referer = request.META.get('HTTP_REFERER')
        if referer and '/applications/' in referer:
            return redirect('recruitment:application_detail', pk=application.id)
        else:
            return redirect('recruitment:application_management')
    
    # If not POST, redirect to application detail
    return redirect('recruitment:application_detail', pk=application.id)

@login_required
@user_passes_test(is_hr_staff)
def export_applications(request):
    """Export applications to CSV"""
    # Get filtered applications based on request parameters
    applications = Application.objects.all().order_by('-created_at')
    
    # Apply the same filters as in application_management view
    position = request.GET.get('position', '')
    if position:
        applications = applications.filter(position_id=position)
    
    status = request.GET.get('status', '')
    if status:
        applications = applications.filter(status=status)
    
    search = request.GET.get('search', '')
    if search:
        applications = applications.filter(
            Q(candidate__name__icontains=search) |
            Q(candidate__email__icontains=search)
        )
    
    # Create the HttpResponse object with CSV header
    response = HttpResponse(content_type='text/csv')
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    response['Content-Disposition'] = f'attachment; filename="applications_export_{timestamp}.csv"'
    
    # Create CSV writer
    writer = csv.writer(response)
    writer.writerow(['ID', 'Candidate Name', 'Email', 'Phone', 'Position', 'Department', 'Status', 'Applied On'])
    
    # Add application data
    for app in applications:
        writer.writerow([
            app.id,
            app.candidate.name,
            app.candidate.email,
            app.candidate.phone,
            app.position.title,
            app.position.department,
            app.get_status_display(),
            app.created_at.strftime('%Y-%m-%d %H:%M')
        ])
    
    return response

@login_required
def interview_calendar(request):
    """View for displaying interview calendar"""
    return render(request, 'recruitment/interview_calendar.html')

@login_required
def get_interview_events(request):
    """API endpoint to get interview events for calendar"""
    start = request.GET.get('start', None)
    end = request.GET.get('end', None)
    
    if start and end:
        start_date = datetime.fromisoformat(start.replace('Z', '+00:00'))
        end_date = datetime.fromisoformat(end.replace('Z', '+00:00'))
        
        interviews = Interview.objects.filter(
            scheduled_date__gte=start_date,
            scheduled_date__lte=end_date
        )
        
        events = []
        for interview in interviews:
            # Xác định màu dựa trên trạng thái
            color = {
                'scheduled': '#3498db',  # Xanh dương
                'completed': '#2ecc71',  # Xanh lá
                'cancelled': '#e74c3c',  # Đỏ
                'rescheduled': '#f1c40f'  # Vàng
            }.get(interview.status, '#95a5a6')  # Xám mặc định
            
            events.append({
                'id': interview.id,
                'title': f"Interview: {interview.candidate.name}",
                'start': interview.scheduled_date.isoformat(),
                'end': (interview.scheduled_date + timedelta(hours=1)).isoformat(),
                'color': color,
                'url': reverse('recruitment:interview_detail', args=[interview.id]),
                'extendedProps': {
                    'candidate': interview.candidate.name,
                    'position': interview.position.title,
                    'status': interview.status,
                    'interviewer': interview.interviewer.get_full_name() if interview.interviewer else 'Not assigned'
                }
            })
        
        return JsonResponse(events, safe=False)
    
    return JsonResponse([], safe=False)

@login_required
@user_passes_test(is_hr_staff)
def schedule_interview(request):
    """View for scheduling a new interview"""
    if request.method == 'POST':
        form = InterviewScheduleForm(request.POST)
        if form.is_valid():
            interview = form.save()
            # Gửi email thông báo
            try:
                from .utils import send_interview_notification
                send_interview_notification(interview)
                messages.success(request, 'Lịch phỏng vấn đã được tạo và email thông báo đã được gửi.')
            except Exception as e:
                messages.warning(request, f'Lịch phỏng vấn đã được tạo nhưng không thể gửi email: {str(e)}')
            return redirect('recruitment:interview_calendar')
    else:
        form = InterviewScheduleForm()
    
    return render(request, 'recruitment/schedule_interview.html', {'form': form})

def confirm_interview(request, interview_id):
    """View để gửi lại email xác nhận tham gia phỏng vấn"""
    interview = get_object_or_404(Interview, id=interview_id)
    
    try:
        from .utils import send_interview_confirmation
        send_interview_confirmation(interview)
        messages.success(request, 'Đã gửi lại email xác nhận tham gia phỏng vấn thành công.')
    except Exception as e:
        messages.error(request, f'Không thể gửi email xác nhận: {str(e)}')
    
    # Chuyển hướng về trang chủ
    return redirect('recruitment:home')

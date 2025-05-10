from django.db import models
from django.contrib.auth.models import User

class Candidate(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=20)
    resume = models.FileField(upload_to='resumes/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

# Thêm vào model Position

class Position(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    requirements = models.TextField()
    salary_range = models.CharField(max_length=100, blank=True, null=True)  # Thêm trường lương
    department = models.CharField(max_length=100, blank=True, null=True)  # Thêm phòng ban
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title
    
    EMPLOYMENT_TYPES = [
        ('full_time', 'Full-time'),
        ('part_time', 'Part-time'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
        ('internship', 'Internship'),
        ('remote', 'Remote'),
    ]
    
    employment_type = models.CharField(
        max_length=20, 
        choices=EMPLOYMENT_TYPES, 
        default='full_time',
        verbose_name='Employment Type'
    )
    
    def __str__(self):
        return self.title

class Application(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending Review'),
        ('reviewing', 'Under Review'),
        ('interview', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='applications')
    position = models.ForeignKey(Position, on_delete=models.CASCADE, related_name='applications')
    cover_letter = models.TextField(blank=True)
    resume = models.FileField(upload_to='resumes/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    def __str__(self):
        return f"{self.candidate.name} - {self.position.title}"

class Interview(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    INTERVIEW_TYPES = [
        ('phone', 'Phone Interview'),
        ('video', 'Video Interview'),
        ('technical', 'Technical Interview'),
        ('onsite', 'On-site Interview'),
        ('assessment', 'Assessment'),
    ]
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
    duration = models.IntegerField(help_text='Duration in minutes', default=60)
    interview_type = models.CharField(max_length=20, choices=INTERVIEW_TYPES, default='onsite')
    location = models.CharField(max_length=200, blank=True, null=True, help_text='Địa điểm phỏng vấn')
    notes = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    feedback = models.TextField(blank=True, null=True)
    rating = models.IntegerField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.candidate.name} - {self.position.title}"

class UserProfile(models.Model):
    USER_TYPES = [
        ('candidate', 'Candidate'),
        ('hr', 'HR Staff'),
        ('interviewer', 'Interviewer'),
        ('admin', 'Administrator'),
    ]
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    user_type = models.CharField(max_length=20, choices=USER_TYPES, default='candidate')
    department = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.get_user_type_display()}"


# Thêm model này vào file models.py hiện có

class ApplicationStatusHistory(models.Model):
    application = models.ForeignKey(Application, on_delete=models.CASCADE, related_name='status_history')
    previous_status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES, null=True, blank=True)
    new_status = models.CharField(max_length=20, choices=Application.STATUS_CHOICES)
    notes = models.TextField(blank=True, null=True)
    updated_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.application.candidate.name} - {self.new_status} - {self.created_at.strftime('%Y-%m-%d')}"
    
    def get_new_status_display(self):
        return dict(Application.STATUS_CHOICES).get(self.new_status, self.new_status)

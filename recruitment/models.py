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
    
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)
    interviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField()
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

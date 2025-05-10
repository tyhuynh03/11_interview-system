from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Candidate, Position, Interview

class CandidateForm(forms.ModelForm):
    class Meta:
        model = Candidate
        fields = ['name', 'email', 'phone', 'resume']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
            'resume': forms.FileInput(attrs={'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'}),
        }


class CandidateRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    }))
    first_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    }))
    last_name = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    }))
    phone = forms.CharField(required=True, widget=forms.TextInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    }))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2')
        
    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            # Create a candidate profile for this user
            Candidate.objects.create(
                user=user,
                name=f"{user.first_name} {user.last_name}",
                email=user.email,
                phone=self.cleaned_data['phone']
            )
        
        return user

class ApplicationForm(forms.Form):
    cover_letter = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500',
        'rows': 5
    }))
    resume = forms.FileField(widget=forms.FileInput(attrs={
        'class': 'w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500'
    }))


class PositionForm(forms.ModelForm):
    class Meta:
        model = Position
        fields = ['title', 'department', 'salary_range', 'employment_type', 'description', 'requirements', 'is_active']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5, 'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
            'requirements': forms.Textarea(attrs={'rows': 5, 'class': 'shadow-sm focus:ring-indigo-500 focus:border-indigo-500 block w-full sm:text-sm border-gray-300 rounded-md'}),
        }

class InterviewScheduleForm(forms.ModelForm):
    class Meta:
        model = Interview
        fields = ['candidate', 'position', 'interviewer', 'scheduled_date', 'duration', 'interview_type', 'location', 'notes']
        widgets = {
            'candidate': forms.Select(attrs={
                'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'
            }),
            'position': forms.Select(attrs={
                'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'
            }),
            'interviewer': forms.Select(attrs={
                'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'
            }),
            'scheduled_date': forms.DateTimeInput(attrs={
                'type': 'datetime-local',
                'class': 'mt-1 block w-full border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'
            }),
            'duration': forms.NumberInput(attrs={
                'min': '15',
                'max': '180',
                'step': '15',
                'class': 'mt-1 block w-full border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'
            }),
            'interview_type': forms.Select(attrs={
                'class': 'mt-1 block w-full pl-3 pr-10 py-2 text-base border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'
            }),
            'location': forms.TextInput(attrs={
                'class': 'mt-1 block w-full border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md',
                'placeholder': 'Nhập địa điểm phỏng vấn'
            }),
            'notes': forms.Textarea(attrs={
                'rows': 4,
                'class': 'mt-1 block w-full border-gray-300 focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm rounded-md'
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hiển thị tất cả ứng viên
        self.fields['candidate'].queryset = Candidate.objects.all()
        
        # Lọc danh sách vị trí chỉ hiển thị những vị trí đang mở
        self.fields['position'].queryset = Position.objects.filter(is_active=True)
        
        # Lọc danh sách người phỏng vấn chỉ hiển thị HR và Interviewer
        self.fields['interviewer'].queryset = User.objects.filter(
            profile__user_type__in=['hr', 'interviewer', 'admin']
        )
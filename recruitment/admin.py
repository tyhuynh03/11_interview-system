from django.contrib import admin
from .models import Candidate, Position, Interview

@admin.register(Candidate)
class CandidateAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'created_at')
    search_fields = ('name', 'email')

@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('title', 'description')

@admin.register(Interview)
class InterviewAdmin(admin.ModelAdmin):
    list_display = ('candidate', 'position', 'interviewer', 'scheduled_date', 'status')
    list_filter = ('status', 'position')
    search_fields = ('candidate__name', 'position__title')

from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings
from django.utils.html import strip_tags

def send_interview_notification(interview):
    """
    Gửi email thông báo lịch phỏng vấn cho ứng viên
    """
    subject = f'Thông Báo Lịch Phỏng Vấn - {interview.position.title}'
    
    # Chuẩn bị context cho template
    context = {
        'candidate_name': interview.candidate.name,
        'position_title': interview.position.title,
        'interview_time': interview.scheduled_date.strftime('%H:%M %d/%m/%Y'),
        'interview_location': interview.location if hasattr(interview, 'location') else 'Chưa cập nhật',
        'interviewer_name': interview.interviewer.get_full_name() if interview.interviewer else 'Chưa cập nhật',
        'site_url': settings.SITE_URL,
        'company_name': settings.COMPANY_NAME,
    }
    
    # Render template HTML
    html_message = render_to_string('recruitment/email/interview_notification.html', context)
    plain_message = strip_tags(html_message)
    
    # Gửi email
    send_mail(
        subject=subject,
        message=plain_message,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[interview.candidate.email],
        html_message=html_message,
        fail_silently=False,
    )

def send_interview_confirmation(interview):
    """Gửi email xác nhận tham gia phỏng vấn cho HR"""
    subject = f'Xác nhận tham gia phỏng vấn - {interview.position.title}'
    
    # Render template email
    html_message = render_to_string('recruitment/email/interview_confirmation.html', {
        'interview': interview,
    })
    
    # Gửi email cho HR
    send_mail(
        subject=subject,
        message=strip_tags(html_message),  # Plain text version
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[settings.EMAIL_HOST_USER],  # Gửi cho HR
        html_message=html_message,
        fail_silently=False,
    ) 
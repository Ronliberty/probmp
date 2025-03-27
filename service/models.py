import uuid
from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail

User = settings.AUTH_USER_MODEL


class Service(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField()
    sample_website = models.URLField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='created_services', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-created_at']


class ServiceRequestQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_deleted=False)


class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('in_progress', 'In Progress'),
        ('on_hold', 'On Hold'),
        ('completed', 'Completed'),
        ('canceled', 'Canceled'),
    ]

    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    country = models.CharField(max_length=100, blank=True, null=True)
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name='requests')
    requested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='service_requests')
    additional_details = models.TextField(blank=True, null=True, verbose_name="Description")
    requested_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True, blank=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_deleted = models.BooleanField(default=False)

    objects = ServiceRequestQuerySet.as_manager()

    def __str__(self):
        return f"Request {self.id} for {self.service.name} by {self.requested_by.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.service.name}-{uuid.uuid4().hex[:6]}")
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-requested_at']


class ServiceResponse(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    service_request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE, related_name='responses')
    responded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='responses')
    status = models.CharField(
        max_length=50,
        choices=[
            ('approved', 'Approved'),
            ('rejected', 'Rejected'),
            ('in_progress', 'In Progress'),
            ('on_hold', 'On Hold'),
            ('completed', 'Completed'),
            ('canceled', 'Canceled'),
        ],
        default='in_progress',
    )
    description = models.TextField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)
    responded_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        """ Automatically update the service request status when a response is made """
        super().save(*args, **kwargs)  # Save the response first

        # Update the related service request status
        self.service_request.status = self.status
        self.service_request.save()

    def __str__(self):
        return f"Response to {self.service_request.id} by {self.responded_by.email}"

    class Meta:
        ordering = ['-responded_at']


# -------- SIGNALS FOR STATUS UPDATES & EMAILS -------- #
@receiver(post_save, sender=ServiceRequest)
def send_service_request_status_email(sender, instance, **kwargs):
    """Send email when a service request's status changes."""
    if instance.pk:  # Ensure the request already exists
        old_instance = ServiceRequest.objects.get(pk=instance.pk)
        if old_instance.status != instance.status:
            subject = f"Your Service Request for {instance.service.name} is now {instance.status.upper()}"
            message = f"""
            Hello {instance.requested_by.first_name},

            Your request for the service '{instance.service.name}' has been updated to: {instance.status.upper()}.

            Details:
            - Requested Service: {instance.service.name}
            - Status: {instance.status}
            - Priority: {instance.priority}
            - Additional Details: {instance.additional_details or 'N/A'}

            If you have any questions, please contact support.

            Thank you,
            Your Team
            """
            send_mail(
                subject,
                message,
                'no-reply@yourdomain.com',
                [instance.requested_by.email],
                fail_silently=False,
            )


@receiver(post_save, sender=ServiceResponse)
def send_service_response_email(sender, instance, **kwargs):
    """Send email when a response is made to a service request."""
    subject = f"Update on Your Service Request - {instance.service_request.service.name}"
    message = f"""
    Hello {instance.service_request.requested_by.first_name},

    Your service request for '{instance.service_request.service.name}' has been updated.

    New Status: {instance.status.upper()}
    Response: {instance.description or 'No additional details provided.'}
    {f"More details: {instance.link}" if instance.link else ''}

    If you have questions, please contact support.

    Thank you,
    Support Team
    """
    send_mail(
        subject,
        message,
        'no-reply@yourdomain.com',
        [instance.service_request.requested_by.email],
        fail_silently=False,
    )

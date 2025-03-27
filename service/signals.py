from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import ServiceResponse, ServiceRequest
from custom_account.models import Notification  # Import Notification model if notifications are required

@receiver(post_save, sender=ServiceResponse)
def update_service_request_status(sender, instance, created, **kwargs):
    """
    Update the related ServiceRequest status based on the ServiceResponse status.
    If a response is approved, rejected, in progress, or completed, update the request accordingly.
    """
    service_request = instance.service_request
    service_request.status = instance.status
    service_request.save()

    # Send notification when a response is added
    Notification.objects.create(
        user=service_request.requested_by,  # Notify the user who requested the service
        message=f"Your service request for '{service_request.service.name}' has been updated to {instance.status.upper()}.",
    )

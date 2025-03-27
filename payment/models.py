from django.db import models
from django.conf import settings
from django.utils import timezone
from django.utils.text import slugify
import uuid  # For unique invoice ID

User = settings.AUTH_USER_MODEL


class Invoice(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('canceled', 'Canceled'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)  # Unique invoice ID
    amount_to_pay = models.DecimalField(max_digits=12, decimal_places=2)
    description = models.TextField()
    wallet_email_or_account = models.CharField(max_length=255)
    recipient_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="invoices")
    created_by = models.ForeignKey(User, related_name='created_invoices', on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True, null=True)  # Optional payment method
    is_deleted = models.BooleanField(default=False)  # Soft delete support

    def __str__(self):
        return f"Invoice {self.id} - {self.status} - {self.recipient_user.email}"


class Analytics(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='analytics/', blank=True, null=True)
    description = models.TextField()
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    manager = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="created_analytics", null=True, blank=True)
    target_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="analytics")
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True, blank=True)  # Unique slug for reference
    is_deleted = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.target_user.email}-{timezone.now().timestamp()}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Analytics {self.id} for {self.target_user.email} (Created by {self.manager.email if self.manager else 'Unknown'})"

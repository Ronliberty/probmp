import uuid
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.conf import settings


def generate_referral_code():
    """Generate a unique referral code using UUID."""
    return uuid.uuid4().hex

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=150, blank=True, null=True, unique=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    country = models.CharField(max_length=50, blank=True, null=True)
    referral_code = models.CharField(
        max_length=32,
        unique=True,
        default=generate_referral_code,
        editable=False
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  # Only email is required

    # Adding related_name to avoid conflicts with default User model
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',  # Custom related name to avoid conflict
        blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_permissions',  # Custom related name to avoid conflict
        blank=True
    )

    objects = CustomUserManager()

    @property
    def referral_link(self):
        """Generate the referral link using the site's URL and referral code."""
        return f"{settings.SITE_URL}/signup?ref={self.referral_code}"

    def save(self, *args, **kwargs):
        if not self.username:
            self.username = self.email.split('@')[0]  # Auto-generate username from email
        super().save(*args, **kwargs)


class Notification(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)  # The user who receives the notification
    message = models.TextField()  # The notification message
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for when the notification was created
    is_read = models.BooleanField(default=False)  # Track if the notification has been read

    def __str__(self):
        return f"Notification for {self.user.username} - {self.message[:30]}"

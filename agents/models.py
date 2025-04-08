from distutils.command.upload import upload
from enum import unique

from django.db import models
from django.utils.text import slugify
from django.conf import settings
from django.db.models import Max
from django.contrib.auth.models import Group

User = settings.AUTH_USER_MODEL

class OurAgent(models.Model):
    names = models.CharField(max_length=255, blank=True, null=True)
    portfolio = models.TextField(blank=True, null=True)
    email = models.EmailField(max_length=254, blank=True, null=True)
    social_links = models.JSONField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)  # Additional field for bio
    slug = models.SlugField(unique=True, blank=True)  # Slug for SEO-friendly URLs
    active = models.BooleanField(default=True)  # To indicate if the agent is currently available
    created_at = models.DateTimeField(auto_now_add=True)  # Timestamp for agent creation
    updated_at = models.DateTimeField(auto_now=True)  # Timestamp for last update

    def save(self, *args, **kwargs):
        if not self.slug or OurAgent.objects.filter(slug=self.slug).exists():
            base_slug = slugify(self.names)
            unique_slug = base_slug
            count = 1
            while OurAgent.objects.filter(slug=unique_slug).exists():
                unique_slug = f"{base_slug}-{count}"
                count += 1
            self.slug = unique_slug  # Assign unique slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.names or "No name provided"

class AgentImage(models.Model):
    def agent_image_upload_path(instance, filename):
        """Organize images in folders based on agent name."""
        return f"agent_images/{instance.expert.slug}/{filename}"

    expert = models.ForeignKey(OurAgent, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='images/')
    title = models.CharField(max_length=255, blank=True, null=True)  # Optional title for image
    caption = models.TextField(blank=True, null=True)  # Optional caption for image

    def __str__(self):
        return f"Image for {self.expert.names}"

class TicketStatus(models.TextChoices):
    OPEN = 'open', 'Open'
    IN_PROGRESS = 'in_progress', 'In Progress'
    RESOLVED = 'resolved', 'Resolved'
    CLOSED = 'closed', 'Closed'

class TicketPriority(models.TextChoices):
    LOW = 'low', 'Low'
    MEDIUM = 'medium', 'Medium'
    HIGH = 'high', 'High'


class Tickets(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tickets')
    number = models.PositiveIntegerField(unique=True, editable=False)
    subject = models.TextField(max_length=30, blank=False, null=False)
    description = models.TextField(max_length=700, blank=False, null=False)
    assigned_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name="assigned_tickets")
    assigned_group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    priority = models.CharField(
        max_length=20,
        choices=TicketPriority.choices,
        default=TicketPriority.MEDIUM
    )
    status = models.CharField(
        max_length=20,
        choices=TicketStatus.choices,
        default=TicketStatus.OPEN
    )
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self):
        return f"Ticket #{self.number}: {self.subject}"

    def save(self, *args, **kwargs):
        if not self.number:
            last_ticket = Tickets.objects.aggregate(Max("number"))["number__max"]
            self.number = 1 if last_ticket is None else last_ticket + 1


        if not self.slug:
            base_slug = slugify(f"ticket-{self.number}-{self.subject}")
            slug = base_slug
            counter = 1
            while Tickets.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter = slug

            self.slug = slug

        super().save(*args, **kwargs)

class Information(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tutorial')
    name = models.TextField(max_length=30, blank=False, null=False)
    description = models.TextField(max_length=700, blank=False, null=False)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Information.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)



def info_image_path(instance, filename):
    return f'training/information/{instance.information.id}/images/{filename}'
class InformationImage(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to=info_image_path)
    caption = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Image for {self.information.name}"


def info_video_path(instance, filename):
    return f'training/information/{instance.information.id}/videos/{filename}'

class InformationVideo(models.Model):
    information = models.ForeignKey(Information, on_delete=models.CASCADE, related_name="videos")
    video = models.FileField(upload_to=info_video_path)
    title = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"Video for {self.information.name}"
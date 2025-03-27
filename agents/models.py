from django.db import models
from django.utils.text import slugify
from django.conf import settings

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

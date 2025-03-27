from django.db import models
from django.conf import settings
from django.utils.text import slugify
import itertools

User = settings.AUTH_USER_MODEL

class HeroContent(models.Model):
    title = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    subtitle = models.TextField()
    explanation = models.TextField()
    description = models.TextField()
    cta_text = models.CharField(max_length=100)
    cta_link = models.URLField()
    is_active = models.BooleanField(default=True)  # Only active content should be displayed
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='hero', default=1)
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Hero Content"
        verbose_name_plural = "Hero Contents"
        constraints = [
            models.UniqueConstraint(
                fields=['is_active'],
                condition=models.Q(is_active=True),
                name='unique_active_hero_content'
            )
        ]


class Step(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    step_number = models.PositiveIntegerField(unique=True)
    delay = models.PositiveIntegerField(default=200)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)  # Auto-generate slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Step {self.step_number}: {self.title}"

    class Meta:
        ordering = ["step_number"]

class Service(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    icon_url = models.URLField()
    features = models.TextField(blank=True)  # Store features as a text list

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_features_list(self):
        """Return features as a list (split by line break)."""
        return self.features.split("\n") if self.features else []

    def __str__(self):
        return self.title

class Testimonial(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=255)
    image_url = models.URLField()  # URL for the testimonial's profile image
    content = models.TextField()  # Testimonial text
    rating = models.PositiveIntegerField(default=5)  # Star rating (1-5)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = orig = slugify(self.name)
            for x in itertools.count(1):
                if not Testimonial.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f'{orig}-{x}'
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name





class ContactSubmission(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return f"Message from {self.email}"

    def save(self, *args, **kwargs):
        if not self.slug:
            # Generate a base slug from the name
            base_slug = slugify(self.name)
            self.slug = base_slug
            # Ensure uniqueness by appending a number if duplicates exist
            for i in itertools.count(1):
                if not ContactSubmission.objects.filter(slug=self.slug).exists():
                    break
                self.slug = f"{base_slug}-{i}"
        super().save(*args, **kwargs)


class SocialLink(models.Model):
    PLATFORM_CHOICES = [
        ('whatsapp', 'WhatsApp'),
        ('telegram', 'Telegram'),
        ('linkedin', 'LinkedIn'),
        ('twitter', 'Twitter'),
        ('instagram', 'Instagram'),
        ('github', 'GitHub'),
        # Add new platforms here
    ]

    platform = models.CharField(max_length=20, choices=PLATFORM_CHOICES)
    url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.get_platform_display())
            self.slug = base_slug
            counter = 1
            while SocialLink.objects.filter(slug=self.slug).exists():
                self.slug = f"{base_slug}-{counter}"
                counter += 1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.get_platform_display()

    @property
    def icon_name(self):
        # Map platform names to Icons8 icon identifiers
        icon_map = {
            'whatsapp': 'whatsapp',
            'telegram': 'telegram-app',
            'linkedin': 'linkedin',
            'twitter': 'twitter',
            'instagram': 'instagram',
            'github': 'github',
            # Add new mappings here
        }
        return icon_map.get(self.platform, 'link')
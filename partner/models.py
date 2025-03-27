from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.utils import timezone


User = settings.AUTH_USER_MODEL

class Partnership(models.Model):
    """ Represents a partnership entity that can have multiple questions. """
    name = models.CharField(max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_partnerships')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class PartnershipQuestion(models.Model):
    """ Represents a question belonging to a partnership. Can be multiple-choice or descriptive. """
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE, related_name='questions')
    question_text = models.TextField()
    is_multiple_choice = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_questions')

    def __str__(self):
        return f"Question: {self.question_text} ({'Multiple Choice' if self.is_multiple_choice else 'Descriptive'})"

class PartnershipChoice(models.Model):
    """ Represents a choice for multiple-choice questions. """
    question = models.ForeignKey(PartnershipQuestion, on_delete=models.CASCADE, related_name="choices")
    choice_text = models.CharField(max_length=255)

    def __str__(self):
        return f"Choice for '{self.question.question_text}': {self.choice_text}"

class PartnershipAnswer(models.Model):
    """ Stores user answers to questions, supporting both multiple-choice and descriptive answers. """
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE, related_name="answers")
    question = models.ForeignKey(PartnershipQuestion, on_delete=models.CASCADE, related_name="answers")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='answers')
    selected_choices = models.ManyToManyField(PartnershipChoice, blank=True)  # For multiple-choice
    text_answer = models.TextField(blank=True, null=True)  # For descriptive answers
    answered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Answer by {self.user} for {self.question.question_text}"


class PartnershipRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('reviewed', 'Reviewed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partnership_requests')
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE, related_name='requests')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    country = models.CharField(max_length=100, blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='created_requests')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Request by {self.user.email} for {self.partnership.name} ({self.status})"


class AcceptedPartnership(models.Model):
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('completed', 'Completed'),
        ('terminated', 'Terminated'),
    ]

    request = models.OneToOneField(PartnershipRequest, on_delete=models.CASCADE, related_name='accepted_partnership')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='accepted_partnerships')
    partnership = models.ForeignKey(Partnership, on_delete=models.CASCADE, related_name='active_partnerships')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    progress = models.TextField(blank=True, null=True)  # Store progress updates
    started_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def end_partnership(self, status='completed'):
        """ Mark the partnership as ended and store the timestamp """
        self.status = status
        self.ended_at = timezone.now()
        self.save()

    def __str__(self):
        return f"Accepted Partnership: {self.user.email} - {self.partnership.name} ({self.status})"





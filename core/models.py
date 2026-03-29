from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    cover_image = models.ImageField(upload_to='news/', blank=True, null=True)
    attachment = models.FileField(upload_to='news/attachments/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Event(models.Model):
    TYPE_CHOICES = [('match', 'Match'), ('event', 'Event')]
    type = models.CharField(max_length=10, choices=TYPE_CHOICES, default='event')
    title = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField(blank=True, null=True)
    venue = models.CharField(max_length=200, blank=True, null=True)
    opponent = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.title


class Media(models.Model):
    FILE_TYPES = [('image', 'Image'), ('video', 'Video'), ('pdf', 'PDF')]
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='media_uploads/')
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-uploaded_at']

    def __str__(self):
        return self.title


class Announcement(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    amount = models.CharField(max_length=50, blank=True, null=True)
    upi_id = models.CharField(max_length=100, blank=True, null=True)
    qr_code = models.ImageField(upload_to='qr_codes/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class TeamMember(models.Model):
    name = models.CharField(max_length=150)
    role = models.CharField(max_length=100, default='Player')
    photo = models.ImageField(upload_to='team/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    social_facebook = models.URLField(max_length=255, blank=True, null=True)
    social_instagram = models.URLField(max_length=255, blank=True, null=True)
    joined_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['joined_date']

    def __str__(self):
        return self.name
